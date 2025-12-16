"""
Web搜索工具

提供网络搜索和网页内容获取功能。
"""

import json
import asyncio
import aiohttp
from typing import Dict, Any, Optional, List
from urllib.parse import quote, urljoin, urlparse
from bs4 import BeautifulSoup
import re

from tavily import TavilyClient
from src.agent.tools.base_tool import BaseTool, ToolResponse
from src.utils.logger import get_logger
from src.utils.helpers import truncate_text, extract_urls


class WebTool(BaseTool):
    """Web搜索和内容获取工具"""
    
    def __init__(self, api_key: str = ""):
        super().__init__(
            name="web_tool",
            description="进行网络搜索、获取网页内容、提取和分析网页信息"
        )
        self.logger = get_logger("tool.web_tool")
        
        # 初始化Tavily客户端
        self.tavily_client = None
        if api_key:
            try:
                self.tavily_client = TavilyClient(api_key)
                self.logger.info("Tavily client initialized successfully")
            except Exception as e:
                self.logger.error(f"Tavily client initialization failed: {e}")
        
        # 初始化 aiohttp session
        self._session = None
      
    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建 aiohttp session"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self._session = aiohttp.ClientSession(
                timeout=timeout,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
        return self._session
      
    def get_schema(self) -> Dict[str, Any]:
        """获取工具的JSON Schema"""
        return {
            "type": "function",
            "function": {
                "name": "web_tool",
                "description": "进行网络搜索和网页内容获取",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["search", "fetch", "extract", "analyze"],
                            "description": "要执行的操作类型"
                        },
                        "query": {
                            "type": "string",
                            "description": "搜索查询词或URL"
                        },
                        "engine": {
                            "type": "string",
                            "enum": ["tavily"],
                            "description": "搜索引擎（仅用于搜索操作）",
                            "default": "tavily"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "最大结果数量",
                            "default": 10
                        },
                        "extract_type": {
                            "type": "string",
                            "enum": ["text", "links", "images", "tables", "all"],
                            "description": "提取的内容类型",
                            "default": "text"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "请求超时时间（秒）",
                            "default": 15
                        }
                    },
                    "required": ["action", "query"]
                }
            }
        }
    
    async def execute(self, **kwargs) -> ToolResponse:
        """执行Web操作"""
        action = kwargs.get('action')
        query = kwargs.get('query', '').strip()
        
        if not action:
            return ToolResponse(
                success=False,
                message="缺少操作类型参数",
                error="Missing action parameter"
            )
        
        if not query:
            return ToolResponse(
                success=False,
                message="缺少查询词或URL参数",
                error="Missing query parameter"
            )
        
        try:
            if action == 'search':
                engine = kwargs.get('engine', 'tavily')
                max_results = kwargs.get('max_results', 10)
                return await self._search_web(query, engine, max_results)
            
            elif action == 'fetch':
                timeout = kwargs.get('timeout', 15)
                return await self._fetch_url(query, timeout)
            
            elif action == 'extract':
                extract_type = kwargs.get('extract_type', 'text')
                return await self._extract_content(query, extract_type)
            
            elif action == 'analyze':
                return await self._analyze_page(query)
            
            else:
                return ToolResponse(
                    success=False,
                    message=f"不支持的操作类型: {action}",
                    error="Unsupported action"
                )
                
        except Exception as e:
            self.logger.error(f"Web操作失败: {e}")
            return ToolResponse(
                success=False,
                message=f"Web操作失败: {str(e)}",
                error=str(e)
            )
    
    async def _search_web(self, query: str, engine: str, max_results: int) -> ToolResponse:
        """
        执行网络搜索
        
        Args:
            query: 搜索查询词
            engine: 搜索引擎
            max_results: 最大结果数量
            
        Returns:
            搜索结果
        """
        try:
            # 使用Tavily API进行搜索
            if self.tavily_client is None:
                return ToolResponse(
                    success=False,
                    message="Tavily客户端未初始化，请检查API密钥",
                    error="Tavily client not initialized"
                )
            
            # 执行搜索
            search_result = self.tavily_client.search(
                query=query,
                max_results=max_results,
                search_depth="basic",
                include_answer=True
            )
            
            # 转换结果格式
            results = []
            if 'results' in search_result:
                for result in search_result['results']:
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('url', ''),
                        'snippet': result.get('content', ''),
                        'source': 'tavily'
                    })
            
            if not results:
                return ToolResponse(
                    success=True,
                    message=f"未找到搜索结果: {query}",
                    data={'query': query, 'engine': engine, 'results': []}
                )
            
            return ToolResponse(
                success=True,
                message=f"搜索完成，找到 {len(results)} 个结果",
                data={
                    'query': query,
                    'engine': engine,
                    'results': results,
                    'total_results': len(results)
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"搜索失败: {str(e)}",
                error=str(e)
            )
      
    async def _fetch_url(self, url: str, timeout: int) -> ToolResponse:
        """
        获取网页内容
        
        Args:
            url: 网页URL
            timeout: 超时时间
            
        Returns:
            网页内容
        """
        try:
            # 验证URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # 创建HTTP会话
            timeout = aiohttp.ClientTimeout(total=timeout)
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=timeout) as response:
                    if response.status != 200:
                        return ToolResponse(
                            success=False,
                            message=f"无法获取网页，HTTP状态码: {response.status}",
                            error=f"HTTP {response.status}"
                        )
                    
                    # 检查内容类型
                    content_type = response.headers.get('content-type', '').lower()
                    if 'text/html' not in content_type:
                        return ToolResponse(
                            success=False,
                            message=f"不支持的内容类型: {content_type}",
                            error="Unsupported content type"
                        )
                    
                    html = await response.text()
                    
                    # 提取基本信息
                    soup = BeautifulSoup(html, 'html.parser')
                    title = soup.find('title')
                    title_text = title.get_text(strip=True) if title else '无标题'
                    
                    # 提取描述
                    description = ''
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    if meta_desc:
                        description = meta_desc.get('content', '')
                    
                    # 提取主要文本内容
                    main_content = self._extract_main_text(soup)
                    
                    return ToolResponse(
                        success=True,
                        message=f"成功获取网页内容: {title_text}",
                        data={
                            'url': url,
                            'title': title_text,
                            'description': description,
                            'content_length': len(html),
                            'text_length': len(main_content),
                            'content': truncate_text(main_content, 5000),
                            'content_type': content_type,
                            'status_code': response.status
                        }
                    )
                
        except asyncio.TimeoutError:
            return ToolResponse(
                success=False,
                message=f"请求超时（{timeout}秒）",
                error="Request timeout"
            )
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"获取网页失败: {str(e)}",
                error=str(e)
            )
    
    async def _extract_content(self, url: str, extract_type: str) -> ToolResponse:
        """
        提取网页特定内容
        
        Args:
            url: 网页URL
            extract_type: 提取类型
            
        Returns:
            提取的内容
        """
        try:
            # 先获取网页内容
            fetch_result = await self._fetch_url(url, 15)
            if not fetch_result.success:
                return fetch_result
            
            url = fetch_result.data['url']
            
            session = await self._get_session()
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
            
            extracted_data = {}
            
            if extract_type in ['text', 'all']:
                extracted_data['text'] = self._extract_main_text(soup)
            
            if extract_type in ['links', 'all']:
                extracted_data['links'] = self._extract_links(soup, url)
            
            if extract_type in ['images', 'all']:
                extracted_data['images'] = self._extract_images(soup, url)
            
            if extract_type in ['tables', 'all']:
                extracted_data['tables'] = self._extract_tables(soup)
            
            return ToolResponse(
                success=True,
                message=f"成功提取{extract_type}内容",
                data={
                    'url': url,
                    'extract_type': extract_type,
                    'extracted_data': extracted_data
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"内容提取失败: {str(e)}",
                error=str(e)
            )
    
    async def _analyze_page(self, url: str) -> ToolResponse:
        """
        分析网页结构和内容
        
        Args:
            url: 网页URL
            
        Returns:
            分析结果
        """
        try:
            # 获取网页内容
            fetch_result = await self._fetch_url(url, 15)
            if not fetch_result.success:
                return fetch_result
            
            url = fetch_result.data['url']
            
            session = await self._get_session()
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
            
            # 分析页面结构
            analysis = {
                'title': soup.find('title').get_text(strip=True) if soup.find('title') else '无标题',
                'headings': {},
                'links_count': len(soup.find_all('a')),
                'images_count': len(soup.find_all('img')),
                'tables_count': len(soup.find_all('table')),
                'forms_count': len(soup.find_all('form')),
                'scripts_count': len(soup.find_all('script')),
                'stylesheets_count': len(soup.find_all('link', rel='stylesheet')),
                'text_content_length': len(self._extract_main_text(soup)),
                'domain': urlparse(url).netloc,
                'load_time': response.headers.get('x-response-time', 'N/A')
            }
            
            # 统计标题层级
            for i in range(1, 7):
                headings = soup.find_all(f'h{i}')
                analysis['headings'][f'h{i}'] = len(headings)
            
            # 提取主要关键词
            text_content = self._extract_main_text(soup)
            words = re.findall(r'\b\w+\b', text_content.lower())
            word_freq = {}
            for word in words:
                if len(word) > 3:  # 忽略短词
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # 获取前10个高频词
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            analysis['top_keywords'] = [{'word': word, 'count': count} for word, count in top_keywords]
            
            return ToolResponse(
                success=True,
                message=f"页面分析完成: {analysis['title']}",
                data=analysis
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"页面分析失败: {str(e)}",
                error=str(e)
            )
    
    def _extract_main_text(self, soup: BeautifulSoup) -> str:
        """提取网页主要文本内容"""
        # 移除不需要的元素
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        # 获取主要内容
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        
        if main_content:
            text = main_content.get_text(' ', strip=True)
        else:
            # 如果没有找到主要内容区域，获取body的文本
            body = soup.find('body')
            text = body.get_text(' ', strip=True) if body else ''
        
        # 清理文本
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """提取所有链接"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href:
                # 处理相对URL
                if href.startswith('/'):
                    href = urljoin(base_url, href)
                
                links.append({
                    'text': link.get_text(strip=True),
                    'url': href,
                    'title': link.get('title', '')
                })
        
        return links[:50]  # 限制返回数量
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """提取所有图片"""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                # 处理相对URL
                if src.startswith('/'):
                    src = urljoin(base_url, src)
                
                images.append({
                    'src': src,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'width': img.get('width'),
                    'height': img.get('height')
                })
        
        return images[:50]  # 限制返回数量
    
    def _extract_tables(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """提取所有表格"""
        tables = []
        for i, table in enumerate(soup.find_all('table')):
            try:
                # 提取表头
                headers = []
                header_row = table.find('tr')
                if header_row:
                    headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
                
                # 提取表格数据
                rows = []
                for row in table.find_all('tr')[1:]:  # 跳过表头
                    cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                    if cells:
                        rows.append(cells)
                
                tables.append({
                    'table_index': i,
                    'headers': headers,
                    'rows': rows[:10],  # 限制行数
                    'total_rows': len(rows)
                })
                
            except Exception as e:
                self.logger.warning(f"解析表格失败: {e}")
                continue
        
        return tables[:10]  # 限制返回数量
    
    async def close(self):
        """清理资源"""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
  