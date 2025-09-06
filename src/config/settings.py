"""
配置设置管理

负责管理应用程序的配置信息，支持从环境变量和YAML文件加载配置。
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

from .env_loader import load_env, validate_required_env_vars


@dataclass
class AgentConfig:
    """AI代理配置"""
    model: str = ""  # 将从环境变量加载
    base_url: str = ""  # 将从环境变量加载
    api_key: str = ""  # 将从环境变量加载
    max_tokens: int = 4000
    temperature: float = 0.7
    max_conversation_history: int = 10
    
    def __post_init__(self):
        print(f"AgentConfig.__post_init__: model={self.model}, base_url={self.base_url}, api_key={self.api_key}")


@dataclass
class WorkspaceConfig:
    """工作区配置"""
    path: str = "./workspace"
    max_size_mb: int = 100
    auto_cleanup: bool = True


@dataclass
class BrowserConfig:
    """浏览器配置"""
    headless: bool = True
    timeout_seconds: int = 30
    window_size: Dict[str, int] = field(default_factory=lambda: {"width": 1920, "height": 1080})


@dataclass
class SearchConfig:
    """搜索配置"""
    engine: str = "tavily"
    max_results: int = 10
    timeout_seconds: int = 15
    api_key: str = ""


@dataclass
class ToolsConfig:
    """工具配置"""
    file_operations: bool = True
    shell_commands: bool = True
    web_search: bool = True
    browser_automation: bool = True


@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = "INFO"
    file: str = "./suna-lite.log"
    max_size_mb: int = 10
    backup_count: int = 5


@dataclass
class SecurityConfig:
    """安全配置"""
    allow_network: bool = True
    allowed_domains: list = field(default_factory=list)
    block_shell_commands: list = field(default_factory=lambda: ["rm -rf", "format", "del"])


@dataclass
class Settings:
    """应用程序设置"""
    agent: AgentConfig = field(default_factory=AgentConfig)
    workspace: WorkspaceConfig = field(default_factory=WorkspaceConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    search: SearchConfig = field(default_factory=SearchConfig)
    tools: ToolsConfig = field(default_factory=ToolsConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    
    @classmethod
    def load_from_file(cls, config_file: str = "config.yaml") -> "Settings":
        """
        从YAML文件加载配置
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            Settings实例
        """
        config_path = Path(config_file)
        if not config_path.exists():
            print(f"配置文件 {config_file} 不存在，使用默认配置")
            return cls()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            if not config_data:
                return cls()
            
            # 创建各个配置对象
            agent_config = AgentConfig(**config_data.get("agent", {}))
            workspace_config = WorkspaceConfig(**config_data.get("workspace", {}))
            browser_config = BrowserConfig(**config_data.get("browser", {}))
            search_config = SearchConfig(**config_data.get("search", {}))
            tools_config = ToolsConfig(**config_data.get("tools", {}))
            logging_config = LoggingConfig(**config_data.get("logging", {}))
            security_config = SecurityConfig(**config_data.get("security", {}))
            
            return cls(
                agent=agent_config,
                workspace=workspace_config,
                browser=browser_config,
                search=search_config,
                tools=tools_config,
                logging=logging_config,
                security=security_config
            )
            
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            print("使用默认配置")
            return cls()
    
    @classmethod
    def load_from_env(cls) -> "Settings":
        """
        从环境变量加载配置
        
        Returns:
            Settings实例
        """
        env_vars = load_env()
        
        # 验证必需的环境变量
        if not validate_required_env_vars():
            raise ValueError("缺少必需的环境变量")
        
        # 从环境变量创建配置
        print(f"调试: env_vars['OPENAI_API_KEY'] = {env_vars.get('OPENAI_API_KEY')}")
        print(f"调试: env_vars['OPENAI_BASE_URL'] = {env_vars.get('OPENAI_BASE_URL')}")
        
        agent_config = AgentConfig(
            model=env_vars.get("OPENAI_MODEL", ""),
            base_url=env_vars.get("OPENAI_BASE_URL", ""),
            api_key=env_vars.get("OPENAI_API_KEY", ""),
            max_tokens=env_vars.get("MAX_TOKENS", 4000),
            temperature=env_vars.get("TEMPERATURE", 0.7),
            max_conversation_history=env_vars.get("MAX_CONVERSATION_HISTORY", 10)
        )
        
        workspace_config = WorkspaceConfig(
            path=env_vars.get("WORKSPACE_PATH", "./workspace"),
            max_size_mb=env_vars.get("MAX_WORKSPACE_SIZE", 100),
            auto_cleanup=True
        )
        
        browser_config = BrowserConfig(
            headless=env_vars.get("BROWSER_HEADLESS", True),
            timeout_seconds=env_vars.get("BROWSER_TIMEOUT", 30)
        )
        
        search_config = SearchConfig(
            max_results=10,
            timeout_seconds=15
        )
        
        logging_config = LoggingConfig(
            level=env_vars.get("LOG_LEVEL", "INFO"),
            file=env_vars.get("LOG_FILE", "./suna-lite.log")
        )
        
        return cls(
            agent=agent_config,
            workspace=workspace_config,
            browser=browser_config,
            search=search_config,
            tools=ToolsConfig(),
            logging=logging_config,
            security=SecurityConfig()
        )
    
    @classmethod
    def load_with_priority(cls, config_file: str = "config.yaml") -> "Settings":
        """
        从YAML文件加载配置
        
        Args:
            config_file: YAML配置文件路径
            
        Returns:
            Settings实例
        """
        # 1. 首先尝试从YAML文件加载
        if config_file is None:
            config_file = "config.yaml"
        
        config_path = Path(config_file)
        if config_path.exists():
            try:
                settings = cls.load_from_file(config_path)
                print(f"从YAML文件加载配置: {config_file}")
                return settings
            except Exception as e:
                print(f"YAML配置文件加载失败: {e}")
        
        # 2. 如果YAML文件不存在，使用默认配置
        print("使用默认配置（某些功能可能受限）")
        return cls()
    
    def save_to_file(self, config_file: str = "config.yaml") -> None:
        """
        保存配置到文件
        
        Args:
            config_file: 配置文件路径
        """
        config_data = {
            "agent": {
                "model": self.agent.model,
                "base_url": self.agent.base_url,
                "api_key": self.agent.api_key,
                "max_tokens": self.agent.max_tokens,
                "temperature": self.agent.temperature,
                "max_conversation_history": self.agent.max_conversation_history
            },
            "workspace": {
                "path": self.workspace.path,
                "max_size_mb": self.workspace.max_size_mb,
                "auto_cleanup": self.workspace.auto_cleanup
            },
            "browser": {
                "headless": self.browser.headless,
                "timeout_seconds": self.browser.timeout_seconds,
                "window_size": self.browser.window_size
            },
            "search": {
                "engine": self.search.engine,
                "max_results": self.search.max_results,
                "timeout_seconds": self.search.timeout_seconds,
                "api_key": self.search.api_key
            },
            "tools": {
                "file_operations": self.tools.file_operations,
                "shell_commands": self.tools.shell_commands,
                "web_search": self.tools.web_search,
                "browser_automation": self.tools.browser_automation
            },
            "logging": {
                "level": self.logging.level,
                "file": self.logging.file,
                "max_size_mb": self.logging.max_size_mb,
                "backup_count": self.logging.backup_count
            },
            "security": {
                "allow_network": self.security.allow_network,
                "allowed_domains": self.security.allowed_domains,
                "block_shell_commands": self.security.block_shell_commands
            }
        }
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
            print(f"配置已保存到 {config_file}")
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def validate(self) -> bool:
        """
        验证配置的有效性
        
        Returns:
            验证结果
        """
        print(f"调试: agent.api_key = '{self.agent.api_key}'")
        print(f"调试: agent.base_url = '{self.agent.base_url}'")
        print(f"调试: agent.max_tokens = {self.agent.max_tokens} (type: {type(self.agent.max_tokens)})")
        print(f"调试: agent.temperature = {self.agent.temperature} (type: {type(self.agent.temperature)})")
        print(f"调试: workspace.max_size_mb = {self.workspace.max_size_mb} (type: {type(self.workspace.max_size_mb)})")
        print(f"调试: browser.timeout_seconds = {self.browser.timeout_seconds} (type: {type(self.browser.timeout_seconds)})")
        
        # 验证代理配置
        if not self.agent.api_key:
            print("错误：缺少OpenAI API密钥")
            return False
        
        if not self.agent.base_url:
            print("错误：缺少OpenAI Base URL")
            return False
        
        try:
            if self.agent.max_tokens <= 0:
                print("错误：max_tokens必须大于0")
                return False
        except Exception as e:
            print(f"错误：max_tokens比较失败: {e}")
            return False
        
        try:
            if not (0 <= self.agent.temperature <= 2):
                print("错误：temperature必须在0到2之间")
                return False
        except Exception as e:
            print(f"错误：temperature比较失败: {e}")
            return False
        
        # 验证工作区配置
        try:
            if self.workspace.max_size_mb <= 0:
                print("错误：工作区最大大小必须大于0")
                return False
        except Exception as e:
            print(f"错误：workspace.max_size_mb比较失败: {e}")
            return False
        
        # 验证浏览器配置
        try:
            if self.browser.timeout_seconds <= 0:
                print("错误：浏览器超时时间必须大于0")
                return False
        except Exception as e:
            print(f"错误：browser.timeout_seconds比较失败: {e}")
            return False
        
        # 验证搜索配置
        try:
            if self.search.max_results <= 0:
                print("错误：搜索结果数量必须大于0")
                return False
        except Exception as e:
            print(f"错误：search.max_results比较失败: {e}")
            return False
        
        return True