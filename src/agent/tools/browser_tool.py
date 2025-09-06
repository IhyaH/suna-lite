"""
浏览器自动化工具

提供简化的浏览器自动化功能，包括网页导航、元素交互等。
"""

import asyncio
import json
import time
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin, urlparse

from src.agent.tools.base_tool import BaseTool, ToolResponse
from src.utils.logger import get_logger
from src.utils.helpers import truncate_text


class BrowserTool(BaseTool):
    """浏览器自动化工具"""
    
    def __init__(self):
        super().__init__(
            name="browser_tool",
            description="进行浏览器自动化操作，包括网页导航、元素交互、数据提取等"
        )
        self.logger = get_logger("tool.browser_tool")
        
        # 浏览器状态
        self.driver = None
        self.current_url = None
        self.page_title = None
        self.session_history = []
        
        # 配置参数
        self.timeout = 30
        self.headless = True
        self.window_size = (1920, 1080)
        
        # 支持的操作
        self.supported_actions = [
            'navigate', 'click', 'fill', 'submit', 'extract', 'screenshot',
            'back', 'forward', 'refresh', 'get_title', 'get_url', 'find_element'
        ]
    
    def get_schema(self) -> Dict[str, Any]:
        """获取工具的JSON Schema"""
        return {
            "type": "function",
            "function": {
                "name": "browser_tool",
                "description": "进行浏览器自动化操作",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": self.supported_actions,
                            "description": "要执行的操作类型"
                        },
                        "url": {
                            "type": "string",
                            "description": "目标URL（用于navigate操作）"
                        },
                        "selector": {
                            "type": "string",
                            "description": "CSS选择器或XPath（用于元素定位）"
                        },
                        "value": {
                            "type": "string",
                            "description": "要输入的值（用于fill操作）"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "操作超时时间（秒）",
                            "default": 10
                        },
                        "wait_time": {
                            "type": "integer",
                            "description": "等待时间（秒）",
                            "default": 2
                        }
                    },
                    "required": ["action"]
                }
            }
        }
    
    async def execute(self, **kwargs) -> ToolResponse:
        """执行浏览器操作"""
        action = kwargs.get('action')
        
        if not action:
            return ToolResponse(
                success=False,
                message="缺少操作类型参数",
                error="Missing action parameter"
            )
        
        if action not in self.supported_actions:
            return ToolResponse(
                success=False,
                message=f"不支持的操作类型: {action}",
                error="Unsupported action"
            )
        
        try:
            # 确保浏览器已初始化
            if not self.driver:
                await self._initialize_browser()
            
            # 执行相应操作
            if action == 'navigate':
                url = kwargs.get('url')
                if not url:
                    return ToolResponse(
                        success=False,
                        message="缺少URL参数",
                        error="Missing URL parameter"
                    )
                return await self._navigate(url)
            
            elif action == 'click':
                selector = kwargs.get('selector')
                if not selector:
                    return ToolResponse(
                        success=False,
                        message="缺少选择器参数",
                        error="Missing selector parameter"
                    )
                return await self._click_element(selector, kwargs.get('timeout', 10))
            
            elif action == 'fill':
                selector = kwargs.get('selector')
                value = kwargs.get('value', '')
                if not selector:
                    return ToolResponse(
                        success=False,
                        message="缺少选择器参数",
                        error="Missing selector parameter"
                    )
                return await self._fill_form(selector, value, kwargs.get('timeout', 10))
            
            elif action == 'submit':
                selector = kwargs.get('selector')
                return await self._submit_form(selector, kwargs.get('timeout', 10))
            
            elif action == 'extract':
                selector = kwargs.get('selector')
                return await self._extract_content(selector)
            
            elif action == 'screenshot':
                return await self._take_screenshot()
            
            elif action == 'back':
                return await self._go_back()
            
            elif action == 'forward':
                return await self._go_forward()
            
            elif action == 'refresh':
                return await self._refresh_page()
            
            elif action == 'get_title':
                return await self._get_page_title()
            
            elif action == 'get_url':
                return await self._get_current_url()
            
            elif action == 'find_element':
                selector = kwargs.get('selector')
                if not selector:
                    return ToolResponse(
                        success=False,
                        message="缺少选择器参数",
                        error="Missing selector parameter"
                    )
                return await self._find_element(selector)
            
            else:
                return ToolResponse(
                    success=False,
                    message=f"未实现的操作: {action}",
                    error="Action not implemented"
                )
                
        except Exception as e:
            self.logger.error(f"浏览器操作失败: {e}")
            return ToolResponse(
                success=False,
                message=f"浏览器操作失败: {str(e)}",
                error=str(e)
            )
    
    async def _initialize_browser(self) -> bool:
        """
        初始化浏览器
        
        Returns:
            是否成功
        """
        try:
            # 检查是否安装了selenium
            try:
                from selenium import webdriver
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.chrome.options import Options
                from selenium.common.exceptions import WebDriverException, TimeoutException
            except ImportError:
                self.logger.warning("未安装selenium，使用模拟模式")
                self.driver = None
                return True
            
            # 配置Chrome选项
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--window-size={},{}'.format(*self.window_size))
            
            # 设置用户代理
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            
            try:
                # 尝试启动Chrome浏览器
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.set_page_load_timeout(self.timeout)
                
                # 设置隐式等待
                self.driver.implicitly_wait(10)
                
                self.logger.info("浏览器初始化成功")
                return True
                
            except WebDriverException as e:
                self.logger.warning(f"无法启动Chrome浏览器: {e}，使用模拟模式")
                self.driver = None
                return True
                
        except Exception as e:
            self.logger.error(f"浏览器初始化失败: {e}")
            self.driver = None
            return True  # 返回True以便使用模拟模式
    
    async def _navigate(self, url: str) -> ToolResponse:
        """
        导航到指定URL
        
        Args:
            url: 目标URL
            
        Returns:
            导航结果
        """
        try:
            # 如果没有真实的浏览器驱动，使用模拟模式
            if self.driver is None:
                self.current_url = url
                self.page_title = f"模拟页面 - {url}"
                self.session_history.append(url)
                
                return ToolResponse(
                    success=True,
                    message=f"模拟导航到: {url}",
                    data={
                        'url': url,
                        'title': self.page_title,
                        'mode': 'simulation'
                    }
                )
            
            # 真实浏览器导航
            self.driver.get(url)
            
            # 等待页面加载
            await asyncio.sleep(2)
            
            # 更新状态
            self.current_url = self.driver.current_url
            self.page_title = self.driver.title
            self.session_history.append(self.current_url)
            
            return ToolResponse(
                success=True,
                message=f"成功导航到: {url}",
                data={
                    'url': self.current_url,
                    'title': self.page_title,
                    'mode': 'real_browser'
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"导航失败: {str(e)}",
                error=str(e)
            )
    
    async def _click_element(self, selector: str, timeout: int) -> ToolResponse:
        """
        点击元素
        
        Args:
            selector: 元素选择器
            timeout: 超时时间
            
        Returns:
            点击结果
        """
        try:
            if self.driver is None:
                return ToolResponse(
                    success=True,
                    message=f"模拟点击元素: {selector}",
                    data={
                        'selector': selector,
                        'action': 'click',
                        'mode': 'simulation'
                    }
                )
            
            # 查找元素
            element = await self._find_element_by_selector(selector, timeout)
            if not element:
                return ToolResponse(
                    success=False,
                    message=f"未找到元素: {selector}",
                    error="Element not found"
                )
            
            # 点击元素
            element.click()
            
            # 等待页面响应
            await asyncio.sleep(1)
            
            # 更新当前页面信息
            self.current_url = self.driver.current_url
            self.page_title = self.driver.title
            
            return ToolResponse(
                success=True,
                message=f"成功点击元素: {selector}",
                data={
                    'selector': selector,
                    'current_url': self.current_url,
                    'title': self.page_title
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"点击元素失败: {str(e)}",
                error=str(e)
            )
    
    async def _fill_form(self, selector: str, value: str, timeout: int) -> ToolResponse:
        """
        填写表单
        
        Args:
            selector: 表单元素选择器
            value: 要填写的值
            timeout: 超时时间
            
        Returns:
            填写结果
        """
        try:
            if self.driver is None:
                return ToolResponse(
                    success=True,
                    message=f"模拟填写表单: {selector} = {value}",
                    data={
                        'selector': selector,
                        'value': value,
                        'action': 'fill',
                        'mode': 'simulation'
                    }
                )
            
            # 查找元素
            element = await self._find_element_by_selector(selector, timeout)
            if not element:
                return ToolResponse(
                    success=False,
                    message=f"未找到表单元素: {selector}",
                    error="Element not found"
                )
            
            # 清空并填写
            element.clear()
            element.send_keys(value)
            
            return ToolResponse(
                success=True,
                message=f"成功填写表单: {selector}",
                data={
                    'selector': selector,
                    'value': value
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"填写表单失败: {str(e)}",
                error=str(e)
            )
    
    async def _extract_content(self, selector: str = None) -> ToolResponse:
        """
        提取页面内容
        
        Args:
            selector: 可选的选择器，如果提供则提取指定元素的内容
            
        Returns:
            提取的内容
        """
        try:
            if self.driver is None:
                # 模拟模式返回模拟内容
                if selector:
                    content = f"模拟提取的内容 - 选择器: {selector}"
                else:
                    content = f"模拟页面内容 - URL: {self.current_url}"
                
                return ToolResponse(
                    success=True,
                    message="成功提取内容（模拟模式）",
                    data={
                        'content': content,
                        'selector': selector,
                        'mode': 'simulation'
                    }
                )
            
            # 提取内容
            if selector:
                element = await self._find_element_by_selector(selector, 5)
                if not element:
                    return ToolResponse(
                        success=False,
                        message=f"未找到元素: {selector}",
                        error="Element not found"
                    )
                content = element.text
            else:
                # 提取页面主体内容
                body_element = self.driver.find_element(By.TAG_NAME, 'body')
                content = body_element.text
            
            # 截断过长的内容
            content = truncate_text(content, 10000)
            
            return ToolResponse(
                success=True,
                message="成功提取内容",
                data={
                    'content': content,
                    'selector': selector,
                    'content_length': len(content),
                    'mode': 'real_browser'
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"内容提取失败: {str(e)}",
                error=str(e)
            )
    
    async def _find_element_by_selector(self, selector: str, timeout: int):
        """
        根据选择器查找元素
        
        Args:
            selector: 选择器
            timeout: 超时时间
            
        Returns:
            找到的元素或None
        """
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            wait = WebDriverWait(self.driver, timeout)
            
            # 尝试不同的定位策略
            strategies = [
                (By.CSS_SELECTOR, selector),
                (By.XPATH, selector),
                (By.NAME, selector),
                (By.ID, selector),
                (By.CLASS_NAME, selector),
            ]
            
            for by, value in strategies:
                try:
                    element = wait.until(EC.presence_of_element_located((by, value)))
                    return element
                except:
                    continue
            
            return None
            
        except Exception as e:
            self.logger.warning(f"查找元素失败: {e}")
            return None
    
    async def _take_screenshot(self) -> ToolResponse:
        """截取屏幕截图"""
        try:
            if self.driver is None:
                return ToolResponse(
                    success=True,
                    message="模拟截图功能",
                    data={
                        'action': 'screenshot',
                        'mode': 'simulation',
                        'note': '在真实浏览器模式下会保存截图文件'
                    }
                )
            
            # 截图并保存
            import time
            screenshot_path = f"screenshot_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return ToolResponse(
                success=True,
                message=f"截图已保存: {screenshot_path}",
                data={
                    'screenshot_path': screenshot_path,
                    'mode': 'real_browser'
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"截图失败: {str(e)}",
                error=str(e)
            )
    
    async def _get_page_title(self) -> ToolResponse:
        """获取页面标题"""
        try:
            if self.driver is None:
                title = self.page_title or "模拟页面标题"
            else:
                title = self.driver.title
            
            return ToolResponse(
                success=True,
                message=f"页面标题: {title}",
                data={'title': title}
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"获取标题失败: {str(e)}",
                error=str(e)
            )
    
    async def _get_current_url(self) -> ToolResponse:
        """获取当前URL"""
        try:
            if self.driver is None:
                url = self.current_url or "https://example.com"
            else:
                url = self.driver.current_url
            
            return ToolResponse(
                success=True,
                message=f"当前URL: {url}",
                data={'url': url}
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"获取URL失败: {str(e)}",
                error=str(e)
            )
    
    async def _go_back(self) -> ToolResponse:
        """返回上一页"""
        try:
            if self.driver is None:
                return ToolResponse(
                    success=True,
                    message="模拟返回上一页",
                    data={'action': 'back', 'mode': 'simulation'}
                )
            
            self.driver.back()
            await asyncio.sleep(1)
            
            self.current_url = self.driver.current_url
            self.page_title = self.driver.title
            
            return ToolResponse(
                success=True,
                message="成功返回上一页",
                data={
                    'current_url': self.current_url,
                    'title': self.page_title
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"返回失败: {str(e)}",
                error=str(e)
            )
    
    async def _go_forward(self) -> ToolResponse:
        """前进到下一页"""
        try:
            if self.driver is None:
                return ToolResponse(
                    success=True,
                    message="模拟前进到下一页",
                    data={'action': 'forward', 'mode': 'simulation'}
                )
            
            self.driver.forward()
            await asyncio.sleep(1)
            
            self.current_url = self.driver.current_url
            self.page_title = self.driver.title
            
            return ToolResponse(
                success=True,
                message="成功前进到下一页",
                data={
                    'current_url': self.current_url,
                    'title': self.page_title
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"前进失败: {str(e)}",
                error=str(e)
            )
    
    async def _refresh_page(self) -> ToolResponse:
        """刷新页面"""
        try:
            if self.driver is None:
                return ToolResponse(
                    success=True,
                    message="模拟刷新页面",
                    data={'action': 'refresh', 'mode': 'simulation'}
                )
            
            self.driver.refresh()
            await asyncio.sleep(2)
            
            self.current_url = self.driver.current_url
            self.page_title = self.driver.title
            
            return ToolResponse(
                success=True,
                message="成功刷新页面",
                data={
                    'current_url': self.current_url,
                    'title': self.page_title
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"刷新失败: {str(e)}",
                error=str(e)
            )
    
    async def _submit_form(self, selector: str = None, timeout: int = 10) -> ToolResponse:
        """提交表单"""
        try:
            if self.driver is None:
                return ToolResponse(
                    success=True,
                    message=f"模拟提交表单: {selector}",
                    data={
                        'selector': selector,
                        'action': 'submit',
                        'mode': 'simulation'
                    }
                )
            
            if selector:
                element = await self._find_element_by_selector(selector, timeout)
                if not element:
                    return ToolResponse(
                        success=False,
                        message=f"未找到表单元素: {selector}",
                        error="Element not found"
                    )
                element.submit()
            else:
                # 查找并提交第一个表单
                from selenium.webdriver.common.by import By
                form = self.driver.find_element(By.TAG_NAME, 'form')
                form.submit()
            
            await asyncio.sleep(2)
            
            self.current_url = self.driver.current_url
            self.page_title = self.driver.title
            
            return ToolResponse(
                success=True,
                message="成功提交表单",
                data={
                    'selector': selector,
                    'current_url': self.current_url,
                    'title': self.page_title
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"提交表单失败: {str(e)}",
                error=str(e)
            )
    
    async def _find_element(self, selector: str) -> ToolResponse:
        """查找元素"""
        try:
            if self.driver is None:
                return ToolResponse(
                    success=True,
                    message=f"模拟查找元素: {selector}",
                    data={
                        'selector': selector,
                        'found': True,
                        'mode': 'simulation'
                    }
                )
            
            element = await self._find_element_by_selector(selector, 10)
            
            if element:
                element_info = {
                    'tag_name': element.tag_name,
                    'text': truncate_text(element.text, 100),
                    'is_displayed': element.is_displayed(),
                    'is_enabled': element.is_enabled(),
                    'location': element.location,
                    'size': element.size
                }
                
                return ToolResponse(
                    success=True,
                    message=f"找到元素: {selector}",
                    data={
                        'selector': selector,
                        'element_info': element_info,
                        'found': True
                    }
                )
            else:
                return ToolResponse(
                    success=False,
                    message=f"未找到元素: {selector}",
                    data={'selector': selector, 'found': False}
                )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"查找元素失败: {str(e)}",
                error=str(e)
            )
    
    async def close(self):
        """关闭浏览器"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.logger.info("浏览器已关闭")
            except Exception as e:
                self.logger.error(f"关闭浏览器失败: {e}")
    
    def __del__(self):
        """析构函数"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass