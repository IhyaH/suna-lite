"""
Suna-Lite 主入口点

提供命令行界面和交互式对话功能。
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import Settings
from src.utils.logger import setup_logging, get_logger
from src.agent import SunaAgent
from src.workspace import WorkspaceManager


class SunaCLI:
    """Suna-Lite 命令行界面"""
    
    def __init__(self):
        self.console = Console()
        self.settings: Optional[Settings] = None
        self.agent: Optional[SunaAgent] = None
        self.workspace_manager: Optional[WorkspaceManager] = None
        self.logger = None
        
    def initialize(self, config_file: Optional[str] = None) -> bool:
        """
        初始化应用程序
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            是否成功
        """
        try:
            # 加载配置（使用YAML配置文件）
            self.settings = Settings.load_with_priority(config_file)
            
            # 验证配置
            if not self.settings.validate():
                self.console.print("配置验证失败", style="red")
                return False
            
            # 设置日志
            setup_logging(
                level=self.settings.logging.level,
                log_file=self.settings.logging.file,
                max_size_mb=self.settings.logging.max_size_mb,
                backup_count=self.settings.logging.backup_count
            )
            self.logger = get_logger("suna-lite")
            
            # 初始化工作区管理器
            self.workspace_manager = WorkspaceManager(self.settings.workspace)
            self.workspace_manager.initialize()
            
            # 初始化AI代理
            self.agent = SunaAgent(self.settings, self.workspace_manager)
            
            self.console.print("Suna-Lite 初始化完成", style="green")
            return True
            
        except Exception as e:
            self.console.print(f"初始化失败: {e}", style="red")
            return False
    
    def show_banner(self):
        """显示欢迎横幅"""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                    Suna-Lite v0.1.0                           ║
║              简化版AI代理系统 - 本地运行                        ║
║                    作者: Suna-Lite Team                       ║
╚═══════════════════════════════════════════════════════════════╝
        """
        self.console.print(banner, style="cyan")
        
        # 显示系统信息
        info_text = """
**AI代理**: 基于 OpenAI API 的智能对话助手
**文件操作**: 读写文件、目录管理
**命令执行**: 在安全环境中运行系统命令
**Web搜索**: 使用Tavily API获取最新信息
**浏览器自动化**: 网页交互和数据提取
**工作区管理**: 隔离的任务环境
        """
        self.console.print(Panel(Markdown(info_text), title="功能特性", border_style="blue"))
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
可用命令

基本命令
- `/help` - 显示此帮助信息
- `/clear` - 清空对话历史
- `/reset` - 重置代理状态
- `/exit` - 退出程序

信息查看
- `/workspace` - 显示工作区信息
- `/config` - 显示当前配置
- `/tools` - 显示可用工具说明
- `/history` - 显示对话历史记录
- `/stats` - 显示使用统计信息

管理功能
- `/clean` - 清理工作区临时文件
- `/export` - 导出对话记录到文件

使用示例

文件操作
* "请创建一个名为hello.txt的文件，内容为'Hello World!'"
* "读取当前目录的README.md文件"
* "分析当前目录下的文件类型分布"

Web功能
* "搜索最新的AI发展动态"
* "获取维基百科上Python页面的主要内容"
* "打开百度搜索Suna-Lite"

系统操作
* "查看当前系统的详细信息"
* "安装requests包"
* "检查Python代码的语法错误"

开发辅助
* "用Python写一个计算斐波那契数列的函数"
* "创建一个完整的项目结构"
* "生成数据可视化代码"
        """
        self.console.print(Panel(Markdown(help_text), title="使用帮助", border_style="yellow"))
    
    async def interactive_mode(self):
        """交互式对话模式"""
        self.show_banner()
        # self.show_help()  # 暂时禁用帮助信息显示以避免编码问题
        
        conversation_history = []
        
        while True:
            try:
                # 获取用户输入
                user_input = self.console.input("\n[bold green]你:[/bold green] ").strip()
                
                # 处理特殊命令
                if user_input.startswith('/'):
                    await self.handle_special_command(user_input[1:], conversation_history)
                    continue
                
                if not user_input:
                    continue
                
                # 显示处理中状态
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.console
                ) as progress:
                    task = progress.add_task("思考中...", total=None)
                    
                    # 发送消息给AI代理
                    response = await self.agent.process_message(user_input, conversation_history)
                    
                    progress.remove_task(task)
                
                # 显示AI回复
                self.console.print("\n[bold blue]Suna:[/bold blue]")
                if response.get('success'):
                    self.console.print(Markdown(response['response']))
                else:
                    self.console.print(f"错误: {response.get('error', '未知错误')}", style="red")
                
                # 更新对话历史
                conversation_history.append({
                    'role': 'user',
                    'content': user_input,
                    'timestamp': self.get_current_time()
                })
                
                if response.get('success'):
                    conversation_history.append({
                        'role': 'assistant',
                        'content': response['response'],
                        'timestamp': self.get_current_time()
                    })
                
                # 限制历史记录长度
                if len(conversation_history) > self.settings.agent.max_conversation_history * 2:
                    conversation_history = conversation_history[-self.settings.agent.max_conversation_history * 2:]
                
            except KeyboardInterrupt:
                self.console.print("\n\n再见！", style="yellow")
                break
            except Exception as e:
                self.console.print(f"\n发生错误: {e}", style="red")
                if self.logger:
                    self.logger.error(f"交互模式错误: {e}")
    
    async def handle_special_command(self, command: str, conversation_history: list):
        """处理特殊命令"""
        command = command.lower().strip()
        
        if command == 'help':
            self.show_help()
        
        elif command == 'clear':
            conversation_history.clear()
            self.console.print("对话历史已清空", style="green")
        
        elif command == 'reset':
            if self.agent:
                self.agent.reset()
            self.console.print("代理状态已重置", style="green")
        
        elif command == 'workspace':
            if self.workspace_manager:
                info = self.workspace_manager.get_info()
                self.console.print(Panel(
                    f"工作区路径: {info['path']}\n"
                    f"文件数量: {info['file_count']}\n"
                    f"目录数量: {info['dir_count']}\n"
                    f"总大小: {info['total_size']}",
                    title="工作区信息",
                    border_style="blue"
                ))
        
        elif command == 'config':
            if self.settings:
                config_text = f"""
**AI配置**
- 模型: {self.settings.agent.model}
- 最大令牌: {self.settings.agent.max_tokens}
- 温度: {self.settings.agent.temperature}

**工作区配置**
- 路径: {self.settings.workspace.path}
- 最大大小: {self.settings.workspace.max_size_mb}MB

**工具状态**
- 文件操作: {'启用' if self.settings.tools.file_operations else '禁用'}
- 命令执行: {'启用' if self.settings.tools.shell_commands else '禁用'}
- Web搜索: {'启用' if self.settings.tools.web_search else '禁用'}
- 浏览器自动化: {'启用' if self.settings.tools.browser_automation else '禁用'}
                """
                self.console.print(Panel(Markdown(config_text), title="当前配置", border_style="yellow"))
        
        elif command == 'history':
            await self.show_conversation_history(conversation_history)
        
        elif command == 'stats':
            await self.show_usage_statistics(conversation_history)
        
        elif command == 'tools':
            await self.show_available_tools()
        
        elif command == 'clean':
            await self.clean_workspace()
        
        elif command == 'export':
            await self.export_conversation(conversation_history)
        
        elif command in ['exit', 'quit']:
            raise KeyboardInterrupt()
        
        else:
            self.console.print(f"未知命令: /{command}", style="red")
            self.console.print("输入 /help 查看可用命令", style="dim")
    
    def get_current_time(self):
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    async def show_conversation_history(self, conversation_history: list):
        """显示对话历史"""
        if not conversation_history:
            self.console.print("暂无对话历史", style="dim")
            return
        
        self.console.print(Panel("对话历史", title="对话记录", border_style="blue"))
        
        for i, msg in enumerate(conversation_history, 1):
            role_icon = "[用户]" if msg['role'] == 'user' else "[Suna]"
            role_color = "green" if msg['role'] == 'user' else "blue"
            
            # 截断过长的消息
            content = msg['content']
            if len(content) > 200:
                content = content[:200] + "..."
            
            self.console.print(f"{i}. {role_icon} [{role_color}]{msg['role']}[/{role_color}] ({msg['timestamp']})")
            self.console.print(f"   {content}")
            self.console.print()
    
    async def show_usage_statistics(self, conversation_history: list):
        """显示使用统计"""
        user_messages = [msg for msg in conversation_history if msg['role'] == 'user']
        assistant_messages = [msg for msg in conversation_history if msg['role'] == 'assistant']
        
        total_chars = sum(len(msg['content']) for msg in conversation_history)
        avg_user_length = sum(len(msg['content']) for msg in user_messages) / len(user_messages) if user_messages else 0
        avg_assistant_length = sum(len(msg['content']) for msg in assistant_messages) / len(assistant_messages) if assistant_messages else 0
        
        stats_text = f"""
**使用统计**

**对话统计**
- 总对话轮数: {len(conversation_history)}
- 用户消息数: {len(user_messages)}
- AI回复数: {len(assistant_messages)}

**文本统计**
- 总字符数: {total_chars:,}
- 平均用户消息长度: {avg_user_length:.1f} 字符
- 平均AI回复长度: {avg_assistant_length:.1f} 字符

**会话信息**
- 会话开始时间: {conversation_history[0]['timestamp'] if conversation_history else '无'}
- 最后活动时间: {conversation_history[-1]['timestamp'] if conversation_history else '无'}
        """
        
        self.console.print(Panel(Markdown(stats_text), title="使用统计", border_style="green"))
    
    async def show_available_tools(self):
        """显示可用工具信息"""
        if not self.agent:
            self.console.print("AI代理未初始化", style="red")
            return
        
        tools_info = """
**可用工具**

**文件操作工具**
- 读取文件内容
- 写入和创建文件
- 列出目录内容
- 删除文件和目录
- 复制和移动文件
- 搜索文件

**Shell命令工具**
- 执行系统命令
- 获取系统信息
- 管理文件和目录
- 安装软件包

**Web搜索工具**
- 使用Tavily API搜索网络信息
- 获取网页内容
- 提取页面链接
- 分析页面结构

**浏览器自动化工具**
- 网页导航和交互
- 表单填写和提交
- 元素定位和操作
- 数据提取和抓取

**使用提示**
- 可以通过自然语言指令使用这些工具
- 所有操作都在安全的工作区内进行
- 支持批量操作和自动化脚本
        """
        
        self.console.print(Panel(Markdown(tools_info), title="工具说明", border_style="cyan"))
    
    async def clean_workspace(self):
        """清理工作区"""
        if not self.workspace_manager:
            self.console.print("工作区管理器未初始化", style="red")
            return
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("清理工作区...", total=None)
                
                # 执行清理
                await self.workspace_manager.cleanup()
                
                progress.remove_task(task)
            
            # 显示清理结果
            info = self.workspace_manager.get_info()
            self.console.print("工作区清理完成", style="green")
            self.console.print(f"当前工作区状态: {info['file_count']} 个文件, {info['dir_count']} 个目录")
            
        except Exception as e:
            self.console.print(f"清理失败: {e}", style="red")
            if self.logger:
                self.logger.error(f"工作区清理失败: {e}")
    
    async def export_conversation(self, conversation_history: list):
        """导出对话记录"""
        if not conversation_history:
            self.console.print("暂无对话记录可导出", style="dim")
            return
        
        try:
            # 生成导出文件名
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_export_{timestamp}.md"
            
            # 创建导出内容
            export_content = f"""# Suna-Lite 对话记录导出

**导出时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**对话轮数**: {len(conversation_history)}
**总字符数**: {sum(len(msg['content']) for msg in conversation_history):,}

---

"""
            
            # 添加对话内容
            for msg in conversation_history:
                role_name = "用户" if msg['role'] == 'user' else "Suna"
                role_icon = "[用户]" if msg['role'] == 'user' else "[Suna]"
                
                export_content += f"## {role_icon} {role_name} ({msg['timestamp']})\n\n"
                export_content += f"{msg['content']}\n\n---\n\n"
            
            # 写入文件
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(export_content)
            
            self.console.print(f"对话记录已导出到: {filename}", style="green")
            self.console.print(f"文件大小: {len(export_content):,} 字符", style="dim")
            
        except Exception as e:
            self.console.print(f"导出失败: {e}", style="red")
            if self.logger:
                self.logger.error(f"对话导出失败: {e}")


@click.command()
@click.option('--config', '-c', help='配置文件路径')
@click.option('--debug', is_flag=True, help='启用调试模式')
@click.option('--version', is_flag=True, help='显示版本信息')
def main(config: Optional[str], debug: bool, version: bool):
    """Suna-Lite - 简化版AI代理系统"""
    
    if version:
        console = Console()
        console.print("Suna-Lite v0.1.0", style="cyan")
        return
    
    # 创建CLI实例
    cli = SunaCLI()
    
    # 初始化应用程序
    if not cli.initialize(config):
        sys.exit(1)
    
    # 设置调试模式
    if debug:
        cli.settings.logging.level = "DEBUG"
        setup_logging(
            level="DEBUG",
            log_file=cli.settings.logging.file
        )
    
    # 运行交互模式
    try:
        asyncio.run(cli.interactive_mode())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        cli.console.print(f"程序异常退出: {e}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    main()