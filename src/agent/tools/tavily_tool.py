"""
Tavily工具集合

包含Tavily Python SDK的所有功能：搜索、问答、上下文提取、内容提取、网站爬取和结构映射。
"""

import asyncio
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

from tavily import TavilyClient

from src.agent.tools.base_tool import BaseTool, ToolResponse
from src.utils.logger import get_logger


class TavilyTool(BaseTool):
    """Tavily工具集合 - 包含所有Tavily SDK功能"""
    
    def __init__(self, api_key: str = ""):
        """初始化Tavily工具"""
        super().__init__(
            name="tavily_tool",
            description="Tavily多功能工具集合，包括搜索、问答、内容提取、网站爬取等功能"
        )
        
        self.logger = get_logger(__name__)
        
        # 初始化Tavily客户端
        self.tavily_client = None
        if api_key:
            try:
                self.tavily_client = TavilyClient(api_key)
                self.logger.info("Tavily client initialized successfully")
            except Exception as e:
                self.logger.error(f"Tavily client initialization failed: {e}")
    
    def get_schema(self) -> Dict[str, Any]:
        """获取工具的JSON Schema"""
        return {
            "type": "function",
            "function": {
                "name": "tavily_tool",
                "description": "Tavily多功能工具集合，包括搜索、问答、内容提取、网站爬取等功能",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["search", "qna", "context", "extract", "crawl", "map"],
                            "description": "要执行的操作类型"
                        },
                        "query": {
                            "type": "string",
                            "description": "搜索查询词或URL（根据操作类型而定）"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "最大结果数量（用于搜索和爬取）",
                            "default": 10
                        },
                        "search_depth": {
                            "type": "string",
                            "enum": ["basic", "advanced"],
                            "description": "搜索深度（用于搜索）",
                            "default": "basic"
                        },
                        "include_answer": {
                            "type": "boolean",
                            "description": "是否包含AI生成的答案（用于搜索）",
                            "default": True
                        },
                        "max_depth": {
                            "type": "integer",
                            "description": "最大爬取深度（用于爬取和映射）",
                            "default": 2
                        },
                        "limit": {
                            "type": "integer",
                            "description": "结果数量限制（用于爬取和映射）",
                            "default": 20
                        },
                        "instructions": {
                            "type": "string",
                            "description": "爬取指令（用于爬取和映射）"
                        },
                        "include_images": {
                            "type": "boolean",
                            "description": "是否包含图片（用于内容提取）",
                            "default": False
                        },
                        "urls": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "URL列表（用于内容提取）"
                        }
                    },
                    "required": ["action", "query"]
                }
            }
        }
    
    async def execute(self, **kwargs) -> ToolResponse:
        """执行Tavily操作"""
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
            if self.tavily_client is None:
                return ToolResponse(
                    success=False,
                    message="Tavily客户端未初始化，请检查API密钥",
                    error="Tavily client not initialized"
                )
            
            if action == 'search':
                return await self._search(query, kwargs)
            elif action == 'qna':
                return await self._qna_search(query)
            elif action == 'context':
                return await self._get_search_context(query)
            elif action == 'extract':
                return await self._extract_content(query, kwargs)
            elif action == 'crawl':
                return await self._crawl_website(query, kwargs)
            elif action == 'map':
                return await self._map_website(query, kwargs)
            else:
                return ToolResponse(
                    success=False,
                    message=f"不支持的操作类型: {action}",
                    error="Unsupported action"
                )
                
        except Exception as e:
            self.logger.error(f"Tavily操作失败: {e}")
            return ToolResponse(
                success=False,
                message=f"Tavily操作失败: {str(e)}",
                error=str(e)
            )
    
    async def _search(self, query: str, params: Dict[str, Any]) -> ToolResponse:
        """执行搜索"""
        try:
            max_results = params.get('max_results', 10)
            search_depth = params.get('search_depth', 'basic')
            include_answer = params.get('include_answer', True)
            
            # 执行搜索
            response = self.tavily_client.search(
                query=query,
                max_results=max_results,
                search_depth=search_depth,
                include_answer=include_answer
            )
            
            # 转换结果格式
            results = []
            if 'results' in response:
                for result in response['results']:
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('url', ''),
                        'snippet': result.get('content', ''),
                        'source': 'tavily'
                    })
            
            # 提取AI答案（如果有）
            answer = None
            if include_answer and 'answer' in response:
                answer = response['answer']
            
            return ToolResponse(
                success=True,
                message=f"搜索完成，找到 {len(results)} 个结果",
                data={
                    'query': query,
                    'results': results,
                    'answer': answer,
                    'total_results': len(results)
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"搜索失败: {str(e)}",
                error=str(e)
            )
    
    async def _qna_search(self, query: str) -> ToolResponse:
        """执行问答搜索"""
        try:
            # 执行问答搜索
            answer = self.tavily_client.qna_search(query=query)
            
            return ToolResponse(
                success=True,
                message="问答搜索完成",
                data={
                    'query': query,
                    'answer': answer
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"问答搜索失败: {str(e)}",
                error=str(e)
            )
    
    async def _get_search_context(self, query: str) -> ToolResponse:
        """获取搜索上下文"""
        try:
            # 获取搜索上下文
            context = self.tavily_client.get_search_context(query=query)
            
            return ToolResponse(
                success=True,
                message="搜索上下文获取完成",
                data={
                    'query': query,
                    'context': context
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"搜索上下文获取失败: {str(e)}",
                error=str(e)
            )
    
    async def _extract_content(self, query: str, params: Dict[str, Any]) -> ToolResponse:
        """提取内容"""
        try:
            include_images = params.get('include_images', False)
            
            # 处理URLs
            urls = []
            if ',' in query:
                urls = [url.strip() for url in query.split(',')]
            else:
                urls = [query]
            
            # 验证URL格式
            valid_urls = []
            for url in urls:
                if url.startswith(('http://', 'https://')):
                    valid_urls.append(url)
                else:
                    # 如果不是完整的URL，尝试添加https://
                    valid_urls.append(f'https://{url}')
            
            if not valid_urls:
                return ToolResponse(
                    success=False,
                    message="没有有效的URL",
                    error="No valid URLs"
                )
            
            # 执行内容提取
            response = self.tavily_client.extract(urls=valid_urls, include_images=include_images)
            
            # 处理结果
            extracted_results = []
            failed_results = []
            
            if 'results' in response:
                for result in response['results']:
                    extracted_results.append({
                        'url': result.get('url', ''),
                        'raw_content': result.get('raw_content', ''),
                        'images': result.get('images', [])
                    })
            
            if 'failed_results' in response:
                failed_results = response['failed_results']
            
            return ToolResponse(
                success=True,
                message=f"内容提取完成，成功提取 {len(extracted_results)} 个URL",
                data={
                    'query': query,
                    'extracted_results': extracted_results,
                    'failed_results': failed_results,
                    'total_extracted': len(extracted_results),
                    'total_failed': len(failed_results)
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"内容提取失败: {str(e)}",
                error=str(e)
            )
    
    async def _crawl_website(self, url: str, params: Dict[str, Any]) -> ToolResponse:
        """爬取网站"""
        try:
            max_depth = params.get('max_depth', 2)
            limit = params.get('limit', 20)
            instructions = params.get('instructions', '')
            
            # 执行网站爬取
            response = self.tavily_client.crawl(
                url=url,
                max_depth=max_depth,
                limit=limit,
                instructions=instructions
            )
            
            # 处理结果
            crawled_results = []
            if 'results' in response:
                for result in response['results']:
                    crawled_results.append({
                        'url': result.get('url', ''),
                        'raw_content': result.get('raw_content', ''),
                        'title': result.get('title', '')
                    })
            
            return ToolResponse(
                success=True,
                message=f"网站爬取完成，爬取 {len(crawled_results)} 个页面",
                data={
                    'url': url,
                    'crawled_results': crawled_results,
                    'max_depth': max_depth,
                    'limit': limit,
                    'instructions': instructions,
                    'total_crawled': len(crawled_results)
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"网站爬取失败: {str(e)}",
                error=str(e)
            )
    
    async def _map_website(self, url: str, params: Dict[str, Any]) -> ToolResponse:
        """映射网站结构"""
        try:
            max_depth = params.get('max_depth', 2)
            limit = params.get('limit', 20)
            instructions = params.get('instructions', '')
            
            # 执行网站结构映射
            response = self.tavily_client.map(
                url=url,
                max_depth=max_depth,
                limit=limit,
                instructions=instructions
            )
            
            # 调试：打印响应结构
            self.logger.debug(f"Map response type: {type(response)}")
            self.logger.debug(f"Map response: {response}")
            
            # 处理结果 - Tavily map API可能返回不同的格式
            mapped_results = []
            
            # 如果响应是列表
            if isinstance(response, list):
                for result in response:
                    if isinstance(result, dict):
                        mapped_results.append({
                            'url': result.get('url', ''),
                            'title': result.get('title', '')
                        })
                    elif isinstance(result, str):
                        mapped_results.append({
                            'url': result,
                            'title': ''
                        })
            # 如果响应是字典
            elif isinstance(response, dict):
                if 'results' in response:
                    results = response['results']
                    if isinstance(results, list):
                        for result in results:
                            if isinstance(result, dict):
                                mapped_results.append({
                                    'url': result.get('url', ''),
                                    'title': result.get('title', '')
                                })
                            elif isinstance(result, str):
                                mapped_results.append({
                                    'url': result,
                                    'title': ''
                                })
                else:
                    # 如果没有results字段，直接处理整个响应
                    for key, value in response.items():
                        if isinstance(value, dict):
                            mapped_results.append({
                                'url': value.get('url', ''),
                                'title': value.get('title', '')
                            })
                        elif isinstance(value, str):
                            mapped_results.append({
                                'url': value,
                                'title': ''
                            })
            
            return ToolResponse(
                success=True,
                message=f"网站结构映射完成，发现 {len(mapped_results)} 个页面",
                data={
                    'url': url,
                    'mapped_results': mapped_results,
                    'max_depth': max_depth,
                    'limit': limit,
                    'instructions': instructions,
                    'total_mapped': len(mapped_results),
                    'raw_response': str(response)[:500]  # 保存原始响应用于调试
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"网站结构映射失败: {str(e)}",
                error=str(e)
            )