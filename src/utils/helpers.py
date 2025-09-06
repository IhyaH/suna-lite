"""
辅助函数

提供各种通用的辅助函数。
"""

import os
import re
import json
import hashlib
import mimetypes
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import aiohttp
import asyncio


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    确保目录存在
    
    Args:
        path: 目录路径
        
    Returns:
        Path对象
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def clean_filename(filename: str) -> str:
    """
    清理文件名，移除不安全字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        清理后的文件名
    """
    # 移除或替换不安全字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'[\s]+', '_', filename)
    filename = filename.strip('._')
    
    # 限制文件名长度
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename


def get_file_hash(file_path: Union[str, Path], algorithm: str = 'md5') -> str:
    """
    计算文件哈希值
    
    Args:
        file_path: 文件路径
        algorithm: 哈希算法
        
    Returns:
        哈希值
    """
    hash_obj = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()


def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    获取文件信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件信息字典
    """
    path = Path(file_path)
    stat = path.stat()
    
    return {
        'name': path.name,
        'size': stat.st_size,
        'modified': datetime.fromtimestamp(stat.st_mtime),
        'created': datetime.fromtimestamp(stat.st_ctime),
        'extension': path.suffix,
        'mime_type': mimetypes.guess_type(str(path))[0],
        'is_file': path.is_file(),
        'is_dir': path.is_dir(),
        'is_hidden': path.name.startswith('.'),
        'hash': get_file_hash(path) if path.is_file() else None
    }


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 字节数
        
    Returns:
        格式化后的大小字符串
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def is_safe_path(path: Union[str, Path], base_path: Union[str, Path]) -> bool:
    """
    检查路径是否安全（防止路径遍历攻击）
    
    Args:
        path: 要检查的路径
        base_path: 基础路径
        
    Returns:
        是否安全
    """
    try:
        path = Path(path).resolve()
        base_path = Path(base_path).resolve()
        return str(path).startswith(str(base_path))
    except (OSError, ValueError):
        return False


def sanitize_command(command: str, blocked_commands: List[str]) -> bool:
    """
    检查命令是否安全
    
    Args:
        command: 要检查的命令
        blocked_commands: 被阻止的命令列表
        
    Returns:
        是否安全
    """
    command_lower = command.lower().strip()
    
    for blocked in blocked_commands:
        if blocked.lower() in command_lower:
            return False
    
    return True


def truncate_text(text: str, max_length: int = 1000) -> str:
    """
    截断文本
    
    Args:
        text: 原始文本
        max_length: 最大长度
        
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."


def extract_urls(text: str) -> List[str]:
    """
    从文本中提取URL
    
    Args:
        text: 包含URL的文本
        
    Returns:
        URL列表
    """
    url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
    return re.findall(url_pattern, text)


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并两个字典
    
    Args:
        dict1: 第一个字典
        dict2: 第二个字典
        
    Returns:
        合并后的字典
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def async_timeout(coro, timeout: float):
    """
    为协程添加超时
    
    Args:
        coro: 协程对象
        timeout: 超时时间（秒）
        
    Returns:
        协程结果
    """
    try:
        return asyncio.run(asyncio.wait_for(coro, timeout=timeout))
    except asyncio.TimeoutError:
        raise TimeoutError(f"操作超时，超过 {timeout} 秒")


async def download_file(url: str, save_path: Union[str, Path], timeout: int = 30) -> bool:
    """
    下载文件
    
    Args:
        url: 文件URL
        save_path: 保存路径
        timeout: 超时时间
        
    Returns:
        是否成功
    """
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    save_path = Path(save_path)
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(save_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            f.write(chunk)
                    
                    return True
                else:
                    return False
    except Exception as e:
        print(f"下载文件失败: {e}")
        return False


def parse_json_safely(json_str: str) -> Optional[Dict[str, Any]]:
    """
    安全地解析JSON字符串
    
    Args:
        json_str: JSON字符串
        
    Returns:
        解析后的字典，失败时返回None
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None


def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        是否有效
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def generate_session_id() -> str:
    """
    生成会话ID
    
    Returns:
        会话ID
    """
    import uuid
    return str(uuid.uuid4())


def get_system_info() -> Dict[str, Any]:
    """
    获取系统信息
    
    Returns:
        系统信息字典
    """
    import platform
    import psutil
    
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'cpu_count': psutil.cpu_count(),
        'memory_total': psutil.virtual_memory().total,
        'memory_available': psutil.virtual_memory().available,
        'disk_usage': {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'free': psutil.disk_usage('/').free
        }
    }