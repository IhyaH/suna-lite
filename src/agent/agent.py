"""
Suna-Lite AI代理核心类

实现主要的AI代理功能，包括LLM集成、工具调用和对话管理。
"""

import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

import openai
from src.config.settings import Settings
from src.utils.logger import get_logger
from src.workspace import WorkspaceManager
from src.agent.tools.base_tool import BaseTool, ToolRegistry, ToolResponse
from src.agent.prompts import get_system_prompt


class SunaAgent:
    """Suna-Lite AI代理"""
    
    def __init__(self, settings: Settings, workspace_manager: WorkspaceManager):
        self.settings = settings
        self.workspace_manager = workspace_manager
        self.logger = get_logger("agent")
        
        # 初始化OpenAI客户端
        self.client = openai.AsyncOpenAI(
            base_url=settings.agent.base_url,
            api_key=settings.agent.api_key
        )
        
        # 初始化工具注册表
        self.tool_registry = ToolRegistry()
        
        # 对话状态
        self.conversation_history = []
        self.current_session_id = None
        
        # 系统提示词
        self.system_prompt = get_system_prompt()
        
        self.logger.info("SunaAgent 初始化完成")
    
    async def initialize_tools(self):
        """初始化所有工具"""
        try:
            # 延迟导入以避免循环依赖
            from src.agent.tools.file_tool import FileTool
            from src.agent.tools.shell_tool import ShellTool
            from src.agent.tools.web_tool import WebTool
            from src.agent.tools.tavily_tool import TavilyTool
            from src.agent.tools.browser_tool import BrowserTool
            
            # 创建工具实例
            tools = []
            
            if self.settings.tools.file_operations:
                file_tool = FileTool(self.workspace_manager)
                tools.append(file_tool)
            
            if self.settings.tools.shell_commands:
                shell_tool = ShellTool(self.workspace_manager)
                tools.append(shell_tool)
            
            if self.settings.tools.web_search:
                tavily_tool = TavilyTool(api_key=self.settings.search.api_key)
                tools.append(tavily_tool)
            
            if self.settings.tools.browser_automation:
                browser_tool = BrowserTool()
                tools.append(browser_tool)
            
            # 注册工具
            for tool in tools:
                self.tool_registry.register(tool)
            
            self.logger.info(f"已注册 {len(tools)} 个工具")
            
        except Exception as e:
            self.logger.error(f"初始化工具失败: {e}")
            raise
    
    async def process_message(self, message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        处理用户消息
        
        Args:
            message: 用户消息
            conversation_history: 对话历史
            
        Returns:
            处理结果
        """
        try:
            # 确保工具已初始化
            if not self.tool_registry.tools:
                await self.initialize_tools()
            
            # 构建对话上下文
            messages = self._build_conversation_context(message, conversation_history)
            
            # 获取可用工具的schema
            tool_schemas = self.tool_registry.get_tool_schemas()
            
            # 调用LLM
            response = await self._call_llm(messages, tool_schemas)
            
            # 处理响应
            if response.get('tool_calls'):
                # 执行工具调用
                tool_result = await self._handle_tool_calls(response['tool_calls'])
                
                # 将工具结果添加到对话历史中
                messages.append({
                    'role': 'assistant',
                    'content': response['content']
                })
                
                # 添加工具结果到对话上下文
                messages.append({
                    'role': 'user',
                    'content': f"工具执行结果：\n{tool_result['response']}"
                })
                
                # 重新调用LLM分析工具结果
                final_response = await self._call_llm(messages, [])
                
                return {
                    'success': True,
                    'response': final_response['content'],
                    'tool_results': tool_result['tool_results'],
                    'timestamp': datetime.now().isoformat()
                }
            else:
                # 直接文本响应
                return {
                    'success': True,
                    'response': response['content'],
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"处理消息失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': "抱歉，处理您的请求时发生了错误。"
            }
    
    def _build_conversation_context(self, message: str, conversation_history: List[Dict] = None) -> List[Dict]:
        """
        构建对话上下文
        
        Args:
            message: 当前消息
            conversation_history: 对话历史
            
        Returns:
            对话上下文列表
        """
        messages = []
        
        # 添加系统提示词
        messages.append({
            'role': 'system',
            'content': self.system_prompt
        })
        
        # 添加对话历史
        if conversation_history:
            for msg in conversation_history[-self.settings.agent.max_conversation_history:]:
                messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        # 添加当前消息
        messages.append({
            'role': 'user',
            'content': message
        })
        
        return messages
    
    async def _call_llm(self, messages: List[Dict], tool_schemas: List[Dict] = None) -> Dict[str, Any]:
        """
        调用LLM API
        
        Args:
            messages: 消息列表
            tool_schemas: 工具schema列表
            
        Returns:
            LLM响应
        """
        try:
            # 构建请求参数
            request_params = {
                'model': self.settings.agent.model,
                'messages': messages,
                'max_tokens': self.settings.agent.max_tokens,
                'temperature': self.settings.agent.temperature,
            }
            
            # 添加工具支持
            if tool_schemas:
                request_params['tools'] = tool_schemas
                request_params['tool_choice'] = 'auto'
            
            # 调用API
            response = await self.client.chat.completions.create(**request_params)
            
            # 解析响应
            response_message = response.choices[0].message
            
            result = {
                'content': response_message.content or '',
                'role': response_message.role
            }
            
            # 处理工具调用
            if response_message.tool_calls:
                result['tool_calls'] = []
                for tool_call in response_message.tool_calls:
                    result['tool_calls'].append({
                        'id': tool_call.id,
                        'function': {
                            'name': tool_call.function.name,
                            'arguments': tool_call.function.arguments
                        }
                    })
            
            return result
            
        except Exception as e:
            self.logger.error(f"LLM调用失败: {e}")
            raise
    
    async def _handle_tool_calls(self, tool_calls: List[Dict]) -> Dict[str, Any]:
        """
        处理工具调用
        
        Args:
            tool_calls: 工具调用列表
            
        Returns:
            处理结果
        """
        try:
            results = []
            
            for tool_call in tool_calls:
                function_name = tool_call['function']['name']
                arguments = tool_call['function']['arguments']
                
                # 解析参数
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        arguments = {}
                
                # 执行工具
                tool_response = await self.tool_registry.execute_tool(
                    function_name, **arguments
                )
                
                results.append({
                    'tool_call_id': tool_call['id'],
                    'name': function_name,
                    'response': tool_response.to_dict()
                })
            
            # 构建响应消息
            response_content = self._format_tool_results(results)
            
            return {
                'success': True,
                'response': response_content,
                'tool_results': results,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"处理工具调用失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': "工具执行失败。"
            }
    
    def _format_tool_results(self, results: List[Dict]) -> str:
        """
        格式化工具执行结果
        
        Args:
            results: 工具执行结果列表
            
        Returns:
            格式化的响应文本
        """
        if not results:
            return "没有执行任何工具。"
        
        response_parts = []
        
        for result in results:
            name = result['name']
            response = result['response']
            
            if response['success']:
                response_parts.append(f"✅ **{name}**: {response['message']}")
                
                # 如果有数据，显示数据
                if response.get('data'):
                    data = response['data']
                    if isinstance(data, (dict, list)):
                        data_str = json.dumps(data, ensure_ascii=False, indent=2)
                        response_parts.append(f"```\n{data_str}\n```")
                    else:
                        response_parts.append(f"```\n{data}\n```")
            else:
                response_parts.append(f"❌ **{name}**: {response['message']}")
                if response.get('error'):
                    response_parts.append(f"错误: {response['error']}")
        
        return "\n\n".join(response_parts)
    
    def get_tool_info(self) -> List[Dict[str, Any]]:
        """
        获取工具信息
        
        Returns:
            工具信息列表
        """
        return self.tool_registry.list_tools()
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        获取对话摘要
        
        Returns:
            对话摘要信息
        """
        return {
            'total_messages': len(self.conversation_history),
            'session_id': self.current_session_id,
            'available_tools': len(self.tool_registry.get_available_tools()),
            'model': self.settings.agent.model,
            'workspace_path': self.settings.workspace.path
        }
    
    def reset(self):
        """重置代理状态"""
        self.conversation_history.clear()
        self.current_session_id = None
        self.logger.info("代理状态已重置")
    
    def update_settings(self, new_settings: Settings):
        """
        更新设置
        
        Args:
            new_settings: 新的设置
        """
        self.settings = new_settings
        
        # 更新OpenAI客户端
        self.client = openai.AsyncOpenAI(
            base_url=new_settings.agent.base_url,
            api_key=new_settings.agent.api_key
        )
        
        # 更新系统提示词
        self.system_prompt = get_system_prompt()
        
        self.logger.info("设置已更新")
    
    async def test_connection(self) -> bool:
        """
        测试LLM连接
        
        Returns:
            连接是否成功
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.settings.agent.model,
                messages=[{'role': 'user', 'content': 'Hello'}],
                max_tokens=10
            )
            return True
        except Exception as e:
            self.logger.error(f"LLM连接测试失败: {e}")
            return False