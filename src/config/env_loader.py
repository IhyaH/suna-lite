"""
环境变量加载器

简化版环境变量加载器，现在主要配置从YAML文件加载。
此文件保留用于兼容性和未来的环境变量支持。
"""

import os
from typing import Dict, Any, Optional


def load_env(env_file: Optional[str] = None) -> Dict[str, Any]:
    """
    加载环境变量（简化版）
    
    Args:
        env_file: 环境变量文件路径（已弃用，保留用于兼容性）
        
    Returns:
        包含所有环境变量的字典
    """
    # 返回空字典，因为现在主要使用YAML配置
    return {}


def get_env_var(key: str, default: Any = None) -> Any:
    """
    获取特定环境变量
    
    Args:
        key: 环境变量键名
        default: 默认值
        
    Returns:
        环境变量值
    """
    return os.getenv(key, default)


def validate_required_env_vars() -> bool:
    """
    验证必需的环境变量是否已设置
    现在这个函数总是返回True，因为配置从YAML文件加载
    
    Returns:
        验证结果
    """
    # 现在配置从YAML文件加载，不需要验证环境变量
    return True