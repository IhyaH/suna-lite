"""
工具基类

定义所有工具的基本接口和通用功能。
"""

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

from src.utils.logger import get_logger


class ToolResult(Enum):
    """工具执行结果状态"""
    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"


@dataclass
class ToolResponse:
    """工具响应"""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'success': self.success,
            'message': self.message,
            'data': self.data,
            'error': self.error
        }
    
    def to_json(self) -> str:
        """转换为JSON格式"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class BaseTool(ABC):
    """工具基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = get_logger(f"tool.{name}")
        self.enabled = True
        
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResponse:
        """
        执行工具功能
        
        Args:
            **kwargs: 工具参数
            
        Returns:
            ToolResponse: 执行结果
        """
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        获取工具的JSON Schema
        
        Returns:
            JSON Schema字典
        """
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        验证工具参数
        
        Args:
            params: 参数字典
            
        Returns:
            是否有效
        """
        # 子类可以重写此方法进行参数验证
        return True
    
    def is_available(self) -> bool:
        """
        检查工具是否可用
        
        Returns:
            是否可用
        """
        return self.enabled
    
    def enable(self):
        """启用工具"""
        self.enabled = True
        self.logger.info(f"工具 {self.name} 已启用")
    
    def disable(self):
        """禁用工具"""
        self.enabled = False
        self.logger.info(f"工具 {self.name} 已禁用")
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取工具信息
        
        Returns:
            工具信息字典
        """
        return {
            'name': self.name,
            'description': self.description,
            'enabled': self.enabled,
            'schema': self.get_schema()
        }
    
    async def safe_execute(self, **kwargs) -> ToolResponse:
        """
        安全执行工具（包含错误处理）
        
        Args:
            **kwargs: 工具参数
            
        Returns:
            ToolResponse: 执行结果
        """
        if not self.is_available():
            return ToolResponse(
                success=False,
                message=f"工具 {self.name} 当前不可用",
                error="Tool disabled"
            )
        
        try:
            # 验证参数
            if not self.validate_params(kwargs):
                return ToolResponse(
                    success=False,
                    message=f"参数验证失败: {kwargs}",
                    error="Invalid parameters"
                )
            
            self.logger.info(f"执行工具 {self.name}，参数: {kwargs}")
            
            # 执行工具
            result = await self.execute(**kwargs)
            
            if result.success:
                self.logger.info(f"工具 {self.name} 执行成功")
            else:
                self.logger.warning(f"工具 {self.name} 执行失败: {result.error}")
            
            return result
            
        except Exception as e:
            error_msg = f"工具 {self.name} 执行时发生异常: {str(e)}"
            self.logger.error(error_msg)
            return ToolResponse(
                success=False,
                message="工具执行失败",
                error=str(e)
            )


class ToolRegistry:
    """工具注册表"""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self.logger = get_logger("tool_registry")
    
    def register(self, tool: BaseTool):
        """
        注册工具
        
        Args:
            tool: 工具实例
        """
        self.tools[tool.name] = tool
        self.logger.info(f"注册工具: {tool.name}")
    
    def unregister(self, tool_name: str):
        """
        注销工具
        
        Args:
            tool_name: 工具名称
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
            self.logger.info(f"注销工具: {tool_name}")
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """
        获取工具
        
        Args:
            tool_name: 工具名称
            
        Returns:
            工具实例或None
        """
        return self.tools.get(tool_name)
    
    def get_available_tools(self) -> List[BaseTool]:
        """
        获取所有可用工具
        
        Returns:
            可用工具列表
        """
        return [tool for tool in self.tools.values() if tool.is_available()]
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """
        获取所有工具的Schema
        
        Returns:
            Schema列表
        """
        schemas = []
        for tool in self.get_available_tools():
            schema = tool.get_schema()
            schemas.append(schema)
        return schemas
    
    async def execute_tool(self, tool_name: str, **kwargs) -> ToolResponse:
        """
        执行指定工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            执行结果
        """
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResponse(
                success=False,
                message=f"工具 {tool_name} 不存在",
                error="Tool not found"
            )
        
        return await tool.safe_execute(**kwargs)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        列出所有工具信息
        
        Returns:
            工具信息列表
        """
        return [tool.get_info() for tool in self.tools.values()]
    
    def enable_tool(self, tool_name: str):
        """启用工具"""
        tool = self.get_tool(tool_name)
        if tool:
            tool.enable()
    
    def disable_tool(self, tool_name: str):
        """禁用工具"""
        tool = self.get_tool(tool_name)
        if tool:
            tool.disable()
    
    def clear(self):
        """清空所有工具"""
        self.tools.clear()
        self.logger.info("清空工具注册表")