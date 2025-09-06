"""
Shell命令执行工具

提供在工作区中安全执行系统命令的功能。
"""

import os
import subprocess
import asyncio
import platform
from typing import Dict, Any, Optional, List, Union
from pathlib import Path

from src.agent.tools.base_tool import BaseTool, ToolResponse
from src.workspace import WorkspaceManager
from src.utils.helpers import sanitize_command
from src.utils.logger import get_logger


class ShellTool(BaseTool):
    """Shell命令执行工具"""
    
    def __init__(self, workspace_manager: WorkspaceManager):
        super().__init__(
            name="shell_tool",
            description="在工作区中安全执行系统命令，包括文件操作、程序运行、系统信息查询等"
        )
        self.workspace_manager = workspace_manager
        self.logger = get_logger("tool.shell_tool")
        
        # 获取当前系统信息
        self.system_info = {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'python_version': platform.python_version(),
            'home_directory': Path.home(),
            'current_directory': Path.cwd(),
        }
        
        # 危险命令列表
        self.dangerous_commands = [
            'rm -rf /', 'format', 'del /f /s /q', 'shutdown', 'reboot',
            'halt', 'poweroff', 'mkfs', 'dd if=/dev/zero', 'chmod -R 777 /',
            'chown -R root:root /', 'mv / /dev/null', '> /dev/sda',
            'wget http://malicious', 'curl http://malicious', 'nc -l -p',
            'ncat -l -p', 'socat TCP-LISTEN', 'python -m SimpleHTTPServer'
        ]
        
        # 根据系统添加特定的危险命令
        if self.system_info['platform'] == 'Windows':
            self.dangerous_commands.extend([
                'rmdir /s /q \\', 'del /f /s /q \\*.*', 'format c:',
                'bootrec', 'bcdedit', 'diskpart', 'reg delete'
            ])
        else:
            self.dangerous_commands.extend([
                ':(){ :|:& };:', 'fork bomb', 'sudo rm -rf /',
                'chmod 777 /etc/passwd', 'userdel -r'
            ])
    
    def get_schema(self) -> Dict[str, Any]:
        """获取工具的JSON Schema"""
        return {
            "type": "function",
            "function": {
                "name": "shell_tool",
                "description": "在工作区中安全执行系统命令",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "要执行的命令（可以是单个命令或多个命令用&&连接）"
                        },
                        "working_directory": {
                            "type": "string",
                            "description": "工作目录（相对于工作区）",
                            "default": "."
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "命令执行超时时间（秒）",
                            "default": 30
                        },
                        "capture_output": {
                            "type": "boolean",
                            "description": "是否捕获命令输出",
                            "default": True
                        },
                        "shell": {
                            "type": "boolean",
                            "description": "是否使用shell执行命令",
                            "default": True
                        },
                        "environment": {
                            "type": "object",
                            "description": "环境变量字典",
                            "default": {}
                        }
                    },
                    "required": ["command"]
                }
            }
        }
    
    async def execute(self, **kwargs) -> ToolResponse:
        """执行Shell命令"""
        command = kwargs.get('command', '').strip()
        working_directory = kwargs.get('working_directory', '.')
        timeout = kwargs.get('timeout', 30)
        capture_output = kwargs.get('capture_output', True)
        shell = kwargs.get('shell', True)
        environment = kwargs.get('environment', {})
        
        if not command:
            return ToolResponse(
                success=False,
                message="缺少命令参数",
                error="Missing command parameter"
            )
        
        # 安全检查
        if not self._is_command_safe(command):
            return ToolResponse(
                success=False,
                message="命令被安全策略阻止",
                error="Command blocked by security policy"
            )
        
        try:
            # 解析工作目录
            if working_directory != '.':
                work_dir = self.workspace_manager.resolve_path(working_directory)
            else:
                work_dir = self.workspace_manager.get_session_path()
            
            # 检查工作目录是否存在
            if not work_dir.exists():
                return ToolResponse(
                    success=False,
                    message=f"工作目录不存在: {working_directory}",
                    error="Working directory does not exist"
                )
            
            # 执行命令
            result = await self._execute_command(
                command, 
                work_dir, 
                timeout, 
                capture_output, 
                shell, 
                environment
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"命令执行失败: {e}")
            return ToolResponse(
                success=False,
                message=f"命令执行失败: {str(e)}",
                error=str(e)
            )
    
    def _is_command_safe(self, command: str) -> bool:
        """
        检查命令是否安全
        
        Args:
            command: 要检查的命令
            
        Returns:
            是否安全
        """
        command_lower = command.lower().strip()
        
        # 检查危险命令
        for dangerous in self.dangerous_commands:
            if dangerous.lower() in command_lower:
                self.logger.warning(f"检测到危险命令: {command}")
                return False
        
        # 检查命令注入
        dangerous_chars = [';', '|', '&', '`', '$(', '&&', '||', '>', '>>', '<']
        for char in dangerous_chars:
            if char in command and command.count(char) > 2:  # 允许少量使用
                self.logger.warning(f"检测到可能的命令注入: {command}")
                return False
        
        return True
    
    async def _execute_command(
        self, 
        command: str, 
        work_dir: Path, 
        timeout: int, 
        capture_output: bool, 
        shell: bool, 
        environment: Dict[str, str]
    ) -> ToolResponse:
        """
        执行命令的具体实现
        
        Args:
            command: 命令字符串
            work_dir: 工作目录
            timeout: 超时时间
            capture_output: 是否捕获输出
            shell: 是否使用shell
            environment: 环境变量
            
        Returns:
            执行结果
        """
        try:
            # 准备环境变量
            env = os.environ.copy()
            env.update(environment)
            
            # 添加工作区环境变量
            env['WORKSPACE'] = str(self.workspace_manager.get_session_path())
            env['WORKSPACE_TEMP'] = str(self.workspace_manager.get_temp_path())
            env['WORKSPACE_OUTPUT'] = str(self.workspace_manager.get_output_path())
            
            # 执行命令
            if shell:
                # Windows和Unix使用不同的shell
                if self.system_info['platform'] == 'Windows':
                    shell_cmd = ['cmd.exe', '/c', command]
                else:
                    shell_cmd = ['/bin/bash', '-c', command]
                
                process = await asyncio.create_subprocess_exec(
                    *shell_cmd,
                    cwd=work_dir,
                    env=env,
                    stdout=subprocess.PIPE if capture_output else None,
                    stderr=subprocess.PIPE if capture_output else None,
                    stdin=subprocess.PIPE
                )
            else:
                # 分割命令为参数列表
                cmd_parts = command.split()
                process = await asyncio.create_subprocess_exec(
                    *cmd_parts,
                    cwd=work_dir,
                    env=env,
                    stdout=subprocess.PIPE if capture_output else None,
                    stderr=subprocess.PIPE if capture_output else None,
                    stdin=subprocess.PIPE
                )
            
            # 等待命令完成或超时
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return ToolResponse(
                    success=False,
                    message=f"命令执行超时（{timeout}秒）",
                    error="Command execution timeout"
                )
            
            # 解码输出
            stdout_text = stdout.decode('utf-8', errors='replace').strip() if stdout else ""
            stderr_text = stderr.decode('utf-8', errors='replace').strip() if stderr else ""
            
            # 构建结果
            result_data = {
                'command': command,
                'working_directory': str(work_dir),
                'exit_code': process.returncode,
                'timeout': timeout,
                'platform': self.system_info['platform']
            }
            
            if capture_output:
                result_data['stdout'] = stdout_text
                result_data['stderr'] = stderr_text
            
            # 判断执行结果
            success = process.returncode == 0
            
            if success:
                message = f"命令执行成功"
                if stdout_text:
                    message += f"，输出: {len(stdout_text)} 字符"
            else:
                message = f"命令执行失败，退出码: {process.returncode}"
                if stderr_text:
                    message += f"，错误: {stderr_text[:200]}..."
            
            return ToolResponse(
                success=success,
                message=message,
                data=result_data
            )
            
        except Exception as e:
            return ToolResponse(
                success=False,
                message=f"命令执行异常: {str(e)}",
                error=str(e)
            )
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        获取系统信息
        
        Returns:
            系统信息字典
        """
        return self.system_info.copy()
    
    def get_available_commands(self) -> List[str]:
        """
        获取常用命令列表
        
        Returns:
            命令列表
        """
        common_commands = [
            # 文件操作
            "ls", "dir", "pwd", "cd", "mkdir", "rmdir", "touch", "cp", "mv", "rm",
            # 文本处理
            "cat", "echo", "grep", "find", "head", "tail", "wc", "sort", "uniq",
            # 系统信息
            "uname", "whoami", "date", "time", "ps", "top", "df", "du", "free",
            # 网络相关
            "ping", "curl", "wget", "nslookup", "netstat", "ipconfig", "ifconfig",
            # 开发工具
            "python", "pip", "npm", "node", "git", "gcc", "make", "cmake",
            # 压缩解压
            "tar", "zip", "unzip", "gzip", "gunzip"
        ]
        
        # 根据系统过滤命令
        if self.system_info['platform'] == 'Windows':
            windows_commands = ["dir", "type", "copy", "move", "del", "md", "rd", "cls", "ver"]
            return [cmd for cmd in common_commands + windows_commands if self._command_exists(cmd)]
        else:
            return [cmd for cmd in common_commands if self._command_exists(cmd)]
    
    def _command_exists(self, command: str) -> bool:
        """
        检查命令是否存在
        
        Args:
            command: 命令名称
            
        Returns:
            是否存在
        """
        try:
            if self.system_info['platform'] == 'Windows':
                # Windows使用where命令
                result = subprocess.run(['where', command], capture_output=True, text=True, timeout=5)
            else:
                # Unix使用which或command -v
                result = subprocess.run(['which', command], capture_output=True, text=True, timeout=5)
            
            return result.returncode == 0
        except:
            return False