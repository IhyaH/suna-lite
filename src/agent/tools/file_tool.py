"""
文件操作工具

提供在工作区中进行文件和目录操作的功能。
"""

import os
import mimetypes
from pathlib import Path
from typing import Dict, Any, Optional, Union, List

from src.agent.tools.base_tool import BaseTool, ToolResponse
from src.workspace import WorkspaceManager
from src.utils.helpers import clean_filename, format_file_size
from src.utils.logger import get_logger


class FileTool(BaseTool):
    """文件操作工具"""
    
    def __init__(self, workspace_manager: WorkspaceManager):
        super().__init__(
            name="file_tool",
            description="在工作区中进行文件和目录操作，包括创建、读取、写入、删除、列表等"
        )
        self.workspace_manager = workspace_manager
        self.logger = get_logger("tool.file_tool")
    
    def get_schema(self) -> Dict[str, Any]:
        """获取工具的JSON Schema"""
        return {
            "type": "function",
            "function": {
                "name": "file_tool",
                "description": "在工作区中进行文件和目录操作",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["read", "write", "create", "delete", "list", "info", "copy", "move", "search"],
                            "description": "要执行的操作类型"
                        },
                        "path": {
                            "type": "string",
                            "description": "文件或目录路径（相对于工作区）"
                        },
                        "content": {
                            "type": "string",
                            "description": "要写入的文件内容（仅用于write操作）"
                        },
                        "destination": {
                            "type": "string",
                            "description": "目标路径（用于copy和move操作）"
                        },
                        "pattern": {
                            "type": "string",
                            "description": "搜索模式（用于search操作，支持通配符）"
                        },
                        "recursive": {
                            "type": "boolean",
                            "description": "是否递归操作（用于list和search操作）",
                            "default": False
                        },
                        "encoding": {
                            "type": "string",
                            "description": "文件编码",
                            "default": "utf-8"
                        }
                    },
                    "required": ["action", "path"]
                }
            }
        }
    
    async def execute(self, **kwargs) -> ToolResponse:
        """执行文件操作"""
        action = kwargs.get('action')
        path = kwargs.get('path', '')
        
        if not action:
            return ToolResponse(
                success=False,
                message="缺少操作类型参数",
                error="Missing action parameter"
            )
        
        if not path and action not in ['list']:
            return ToolResponse(
                success=False,
                message="缺少路径参数",
                error="Missing path parameter"
            )
        
        try:
            if action == 'read':
                return await self._read_file(path, kwargs.get('encoding', 'utf-8'))
            elif action == 'write':
                content = kwargs.get('content', '')
                if content is None:
                    content = ''
                return await self._write_file(path, content, kwargs.get('encoding', 'utf-8'))
            elif action == 'create':
                return await self._create_directory(path)
            elif action == 'delete':
                return await self._delete_file_or_directory(path)
            elif action == 'list':
                return await self._list_directory(path, kwargs.get('recursive', False))
            elif action == 'info':
                return await self._get_file_info(path)
            elif action == 'copy':
                destination = kwargs.get('destination')
                if not destination:
                    return ToolResponse(
                        success=False,
                        message="缺少目标路径参数",
                        error="Missing destination parameter"
                    )
                return await self._copy_file(path, destination)
            elif action == 'move':
                destination = kwargs.get('destination')
                if not destination:
                    return ToolResponse(
                        success=False,
                        message="缺少目标路径参数",
                        error="Missing destination parameter"
                    )
                return await self._move_file(path, destination)
            elif action == 'search':
                pattern = kwargs.get('pattern', '*')
                return await self._search_files(pattern, path, kwargs.get('recursive', True))
            else:
                return ToolResponse(
                    success=False,
                    message=f"不支持的操作类型: {action}",
                    error="Unsupported action"
                )
                
        except Exception as e:
            self.logger.error(f"文件操作失败: {e}")
            return ToolResponse(
                success=False,
                message=f"文件操作失败: {str(e)}",
                error=str(e)
            )
    
    async def _read_file(self, path: str, encoding: str) -> ToolResponse:
        """读取文件"""
        try:
            content = self.workspace_manager.read_file(path, encoding)
            if content is None:
                return ToolResponse(
                    success=False,
                    message=f"无法读取文件: {path}",
                    error="File not found or unreadable"
                )
            
            # 检测文件类型
            full_path = self.workspace_manager.resolve_path(path)
            mime_type, _ = mimetypes.guess_type(str(full_path))
            
            # 如果是二进制文件，提供基本信息
            if mime_type and mime_type.startswith('application/'):
                file_info = self.workspace_manager.get_file_info(path)
                return ToolResponse(
                    success=True,
                    message=f"检测到二进制文件，显示基本信息",
                    data={
                        'type': 'binary',
                        'mime_type': mime_type,
                        'size': file_info.get('size', 0) if file_info else 0,
                        'encoding': encoding,
                        'note': '这是一个二进制文件，无法直接显示内容'
                    }
                )
            
            # 限制大文件显示
            if len(content) > 50000:  # 50KB
                preview = content[:5000] + "\n\n... [内容过长，已截断] ..."
                return ToolResponse(
                    success=True,
                    message=f"读取文件成功（内容过长，显示前5000字符）",
                    data={
                        'type': 'text',
                        'content': preview,
                        'full_length': len(content),
                        'encoding': encoding,
                        'note': '文件内容过长，仅显示预览'
                    }
                )
            
            return ToolResponse(
                success=True,
                message=f"读取文件成功",
                data={
                    'type': 'text',
                    'content': content,
                    'length': len(content),
                    'encoding': encoding
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"读取文件失败: {str(e)}",
                error=str(e)
            )
    
    async def _write_file(self, path: str, content: str, encoding: str) -> ToolResponse:
        """写入文件"""
        try:
            # 清理文件名
            path = clean_filename(path)
            
            success = self.workspace_manager.write_file(path, content, encoding)
            if success:
                return ToolResponse(
                    success=True,
                    message=f"写入文件成功: {path}",
                    data={
                        'path': path,
                        'length': len(content),
                        'encoding': encoding
                    }
                )
            else:
                return ToolResponse(
                    success=False,
                    message=f"写入文件失败: {path}",
                    error="Failed to write file"
                )
                
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"写入文件失败: {str(e)}",
                error=str(e)
            )
    
    async def _create_directory(self, path: str) -> ToolResponse:
        """创建目录"""
        try:
            success = self.workspace_manager.create_directory(path)
            if success:
                return ToolResponse(
                    success=True,
                    message=f"创建目录成功: {path}",
                    data={'path': path}
                )
            else:
                return ToolResponse(
                    success=False,
                    message=f"创建目录失败: {path}",
                    error="Failed to create directory"
                )
                
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"创建目录失败: {str(e)}",
                error=str(e)
            )
    
    async def _delete_file_or_directory(self, path: str) -> ToolResponse:
        """删除文件或目录"""
        try:
            full_path = self.workspace_manager.resolve_path(path)
            
            if not full_path.exists():
                return ToolResponse(
                    success=False,
                    message=f"文件或目录不存在: {path}",
                    error="File or directory not found"
                )
            
            if full_path.is_file():
                success = self.workspace_manager.delete_file(path)
                action = "文件"
            else:
                success = self.workspace_manager.delete_directory(path, recursive=True)
                action = "目录"
            
            if success:
                return ToolResponse(
                    success=True,
                    message=f"删除{action}成功: {path}",
                    data={'path': path, 'type': action}
                )
            else:
                return ToolResponse(
                    success=False,
                    message=f"删除{action}失败: {path}",
                    error="Failed to delete"
                )
                
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"删除失败: {str(e)}",
                error=str(e)
            )
    
    async def _list_directory(self, path: str, recursive: bool) -> ToolResponse:
        """列出目录内容"""
        try:
            items = self.workspace_manager.list_directory(path, recursive)
            
            if not items:
                return ToolResponse(
                    success=True,
                    message=f"目录为空或不存在: {path}",
                    data={'items': [], 'path': path, 'recursive': recursive}
                )
            
            # 格式化文件信息
            formatted_items = []
            for item in items:
                formatted_item = {
                    'name': item['name'],
                    'size': format_file_size(item['size']),
                    'size_bytes': item['size'],
                    'modified': item['modified'].strftime('%Y-%m-%d %H:%M:%S') if item['modified'] else 'N/A',
                    'type': 'directory' if item['is_dir'] else 'file',
                    'extension': item['extension'] if item['extension'] else '',
                    'mime_type': item['mime_type'] or 'unknown'
                }
                formatted_items.append(formatted_item)
            
            # 统计信息
            files = [item for item in items if item['is_file']]
            directories = [item for item in items if item['is_dir']]
            total_size = sum(item['size'] for item in files)
            
            return ToolResponse(
                success=True,
                message=f"列出目录成功: {path} ({len(formatted_items)} 项)",
                data={
                    'items': formatted_items,
                    'path': path,
                    'recursive': recursive,
                    'stats': {
                        'total_files': len(files),
                        'total_directories': len(directories),
                        'total_size': format_file_size(total_size),
                        'total_size_bytes': total_size
                    }
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"列出目录失败: {str(e)}",
                error=str(e)
            )
    
    async def _get_file_info(self, path: str) -> ToolResponse:
        """获取文件信息"""
        try:
            info = self.workspace_manager.get_file_info(path)
            if not info:
                return ToolResponse(
                    success=False,
                    message=f"文件不存在: {path}",
                    error="File not found"
                )
            
            # 格式化信息
            formatted_info = {
                'name': info['name'],
                'size': format_file_size(info['size']),
                'size_bytes': info['size'],
                'modified': info['modified'].strftime('%Y-%m-%d %H:%M:%S') if info['modified'] else 'N/A',
                'created': info['created'].strftime('%Y-%m-%d %H:%M:%S') if info['created'] else 'N/A',
                'type': 'directory' if info['is_dir'] else 'file',
                'extension': info['extension'] if info['extension'] else '',
                'mime_type': info['mime_type'] or 'unknown',
                'is_hidden': info['is_hidden'],
                'hash': info['hash'][:16] + '...' if info['hash'] else None
            }
            
            return ToolResponse(
                success=True,
                message=f"获取文件信息成功: {path}",
                data=formatted_info
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"获取文件信息失败: {str(e)}",
                error=str(e)
            )
    
    async def _copy_file(self, src: str, dst: str) -> ToolResponse:
        """复制文件"""
        try:
            success = self.workspace_manager.copy_file(src, dst)
            if success:
                return ToolResponse(
                    success=True,
                    message=f"复制文件成功: {src} -> {dst}",
                    data={'source': src, 'destination': dst}
                )
            else:
                return ToolResponse(
                    success=False,
                    message=f"复制文件失败: {src} -> {dst}",
                    error="Failed to copy file"
                )
                
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"复制文件失败: {str(e)}",
                error=str(e)
            )
    
    async def _move_file(self, src: str, dst: str) -> ToolResponse:
        """移动文件"""
        try:
            success = self.workspace_manager.move_file(src, dst)
            if success:
                return ToolResponse(
                    success=True,
                    message=f"移动文件成功: {src} -> {dst}",
                    data={'source': src, 'destination': dst}
                )
            else:
                return ToolResponse(
                    success=False,
                    message=f"移动文件失败: {src} -> {dst}",
                    error="Failed to move file"
                )
                
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"移动文件失败: {str(e)}",
                error=str(e)
            )
    
    async def _search_files(self, pattern: str, path: str, recursive: bool) -> ToolResponse:
        """搜索文件"""
        try:
            matches = self.workspace_manager.search_files(pattern, path, recursive)
            
            if not matches:
                return ToolResponse(
                    success=True,
                    message=f"未找到匹配的文件: {pattern}",
                    data={'pattern': pattern, 'path': path, 'matches': []}
                )
            
            # 获取匹配文件的详细信息
            detailed_matches = []
            for match in matches:
                file_info = self.workspace_manager.get_file_info(match)
                if file_info:
                    detailed_matches.append({
                        'path': match,
                        'name': file_info['name'],
                        'size': format_file_size(file_info['size']),
                        'size_bytes': file_info['size'],
                        'type': 'directory' if file_info['is_dir'] else 'file',
                        'modified': file_info['modified'].strftime('%Y-%m-%d %H:%M:%S') if file_info['modified'] else 'N/A'
                    })
            
            return ToolResponse(
                success=True,
                message=f"搜索完成，找到 {len(matches)} 个匹配项",
                data={
                    'pattern': pattern,
                    'path': path,
                    'recursive': recursive,
                    'matches': detailed_matches
                }
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"搜索文件失败: {str(e)}",
                error=str(e)
            )