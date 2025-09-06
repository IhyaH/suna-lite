# Suna-Lite 架构文档

本文档详细介绍 Suna-Lite 的系统架构、设计模式和核心组件。

## 总体架构

### 系统层次结构

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI Interface (Rich)                     │
├─────────────────────────────────────────────────────────────┤
│                     SunaAgent Core                          │
├─────────────────────────────────────────────────────────────┤
│   FileTool  │  ShellTool  │  WebTool  │  BrowserTool        │
├─────────────────────────────────────────────────────────────┤
│           Workspace Manager │ Config System                 │
├─────────────────────────────────────────────────────────────┤
│              Logging System │ Utilities                     │
└─────────────────────────────────────────────────────────────┘
```

### 核心设计原则

1. **模块化设计**: 每个功能模块独立且可替换
2. **安全优先**: 所有操作都经过安全验证
3. **异步处理**: 使用 async/await 提高并发性能
4. **可扩展性**: 基于插件化的工具系统
5. **容错性**: 完善的错误处理和恢复机制

## AI 代理核心

### SunaAgent 类结构

```python
class SunaAgent:
    """核心AI代理类，负责协调所有组件"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.tools = self._initialize_tools()
        self.workspace = WorkspaceManager(settings.workspace)
        
    async def process_message(self, message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """处理用户消息的主要入口点"""
```

### 消息处理流程

1. **输入验证**: 验证用户输入和权限
2. **上下文构建**: 构建对话历史和系统提示
3. **LLM 调用**: 向 AI API 发送请求
4. **工具调用**: 解析并执行工具调用
5. **结果整合**: 整合工具结果和AI响应
6. **状态更新**: 更新对话历史和工作区状态

### 工具调用机制

```python
# 工具注册表
self.tools = {
    'file_operations': FileTool(settings),
    'shell_commands': ShellTool(settings),
    'web_search': WebTool(settings),
    'browser_automation': BrowserTool(settings)
}

# 工具调用解析
tool_calls = self._parse_tool_calls(response)
for tool_call in tool_calls:
    tool = self.tools.get(tool_call['name'])
    result = await tool.execute(**tool_call['parameters'])
```

## 工具系统

### 基础工具架构

```python
class BaseTool(ABC):
    """所有工具的抽象基类"""
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResponse:
        """执行工具操作的抽象方法"""
        
    def _validate_params(self, params: Dict[str, Any]) -> bool:
        """验证参数的通用方法"""
        
    def _handle_error(self, error: Exception) -> ToolResponse:
        """统一的错误处理方法"""
```

### 工具注册机制

```python
class ToolRegistry:
    """工具注册和管理系统"""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._tool_schemas: Dict[str, Dict] = {}
        
    def register_tool(self, name: str, tool: BaseTool, schema: Dict):
        """注册新工具"""
        
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """获取工具实例"""
        
    def get_all_schemas(self) -> Dict[str, Dict]:
        """获取所有工具的JSON Schema"""
```

### 文件操作工具

```python
class FileTool(BaseTool):
    """文件系统操作工具"""
    
    # 支持的操作类型
    OPERATIONS = {
        'read': self._read_file,
        'write': self._write_file,
        'create': self._create_file,
        'delete': self._delete_file,
        'list': self._list_directory,
        'copy': self._copy_file,
        'move': self._move_file,
        'search': self._search_files
    }
    
    # 安全特性
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'.txt', '.py', '.md', '.json', '.yaml', '.yml'}
```

### Shell 命令工具

```python
class ShellTool(BaseTool):
    """安全的Shell命令执行工具"""
    
    DANGEROUS_COMMANDS = {
        'rm -rf', 'format', 'del', 'rmdir', 'shutdown',
        'reboot', 'halt', '>', '>>', '|', '&', '&&', '||'
    }
    
    def _is_command_safe(self, command: str) -> bool:
        """验证命令安全性"""
        
    async def _execute_command(self, command: str, timeout: int = 30) -> ToolResponse:
        """执行命令并捕获输出"""
```

### Web 搜索工具

```python
class WebTool(BaseTool):
    """Web搜索和内容获取工具"""
    
    async def _tavily_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Tavily搜索实现"""
        
    async def _fetch_content(self, url: str) -> str:
        """获取网页内容"""
        
    def _extract_links(self, html: str) -> List[Dict[str, str]]:
        """提取页面链接"""
```

### 浏览器自动化工具

```python
class BrowserTool(BaseTool):
    """浏览器自动化工具"""
    
    async def _initialize_browser(self) -> bool:
        """初始化浏览器"""
        
    async def _simulate_navigation(self, url: str) -> Dict[str, Any]:
        """模拟浏览器导航（无头模式）"""
        
    async def _find_element(self, selector: str) -> Dict[str, Any]:
        """查找页面元素"""
```

## 工作区管理

### WorkspaceManager 类

```python
class WorkspaceManager:
    """工作区管理器，提供安全的文件操作环境"""
    
    def __init__(self, config: WorkspaceConfig):
        self.base_path = Path(config.path).resolve()
        self.max_size_mb = config.max_size_mb
        self.auto_cleanup = config.auto_cleanup
        
    def resolve_path(self, path: Union[str, Path]) -> Path:
        """安全解析路径，防止目录遍历攻击"""
        
    def check_size_limit(self, file_size: int) -> bool:
        """检查文件大小限制"""
        
    async def cleanup(self) -> None:
        """清理过期文件"""
```

### 安全机制

1. **路径隔离**: 所有操作限制在工作区内
2. **大小限制**: 防止磁盘空间耗尽
3. **文件类型过滤**: 限制可操作文件类型
4. **自动清理**: 定期清理临时文件

## 配置系统

### 配置层次结构

```
YAML Configuration File
         ↓
   Default Values
```

### Settings 数据类

```python
@dataclass
class Settings:
    """主配置类"""
    agent: AgentConfig
    search: SearchConfig
    workspace: WorkspaceConfig
    browser: BrowserConfig
    tools: ToolsConfig
    logging: LoggingConfig
    security: SecurityConfig
```

### 配置加载流程

```python
def load_settings() -> Settings:
    """加载配置的完整流程"""
    
    # 1. 加载默认配置
    default_config = _get_default_config()
    
    # 2. 加载YAML配置文件
    yaml_config = _load_yaml_config('config.yaml')
    
    # 3. 合并配置
    final_config = _merge_configs(default_config, yaml_config)
    
    # 4. 验证配置
    return _validate_config(final_config)
```

## 日志系统

### 日志配置

```python
class LoggingConfig:
    """日志配置类"""
    
    level: str = "INFO"
    file: Optional[str] = None
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
def setup_logging(config: LoggingConfig):
    """设置日志系统"""
    
    # 创建格式化器
    formatter = logging.Formatter(config.format)
    
    # 设置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 设置文件处理器
    if config.file:
        file_handler = logging.FileHandler(config.file)
        file_handler.setFormatter(formatter)
        
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(config.level)
    root_logger.addHandler(console_handler)
    
    if config.file:
        root_logger.addHandler(file_handler)
```

### 日志级别和用途

- **DEBUG**: 详细的调试信息
- **INFO**: 一般信息性消息
- **WARNING**: 警告信息
- **ERROR**: 错误信息
- **CRITICAL**: 严重错误信息

## 异步处理模式

### 异步模式的优势

1. **并发性**: 可以同时处理多个操作
2. **响应性**: 避免阻塞主线程
3. **资源效率**: 更好的资源利用率
4. **可扩展性**: 易于扩展到高并发场景

### 异步工具执行

```python
async def execute_tool_call(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
    """执行工具调用的异步方法"""
    
    tool_name = tool_call['name']
    parameters = tool_call.get('parameters', {})
    
    try:
        # 获取工具实例
        tool = self.tools.get(tool_name)
        if not tool:
            return {
                'error': f'Unknown tool: {tool_name}',
                'success': False
            }
            
        # 异步执行工具
        result = await tool.execute(**parameters)
        
        # 处理结果
        return {
            'result': result,
            'success': True
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'success': False
        }
```

## 安全架构

### 安全层次

1. **输入验证**: 验证所有用户输入
2. **路径安全**: 防止路径遍历攻击
3. **命令过滤**: 过滤危险的系统命令
4. **权限控制**: 限制文件系统访问
5. **沙箱环境**: 隔离的工作区执行环境

### 安全检查机制

```python
def security_check(operation: str, params: Dict[str, Any]) -> bool:
    """统一的安全检查接口"""
    
    # 1. 输入验证
    if not validate_input(params):
        return False
        
    # 2. 路径安全检查
    if operation in ['file_read', 'file_write']:
        if not is_path_safe(params.get('path', '')):
            return False
            
    # 3. 命令安全检查
    if operation == 'shell_execute':
        if not is_command_safe(params.get('command', '')):
            return False
            
    # 4. 权限检查
    if not check_permissions(operation, params):
        return False
        
    return True
```

## 错误处理

### 错误类型定义

```python
class SunaError(Exception):
    """Suna-Lite基础错误类"""
    pass

class SecurityError(SunaError):
    """安全相关错误"""
    pass

class ConfigurationError(SunaError):
    """配置相关错误"""
    pass

class ToolExecutionError(SunaError):
    """工具执行错误"""
    pass

class WorkspaceError(SunaError):
    """工作区相关错误"""
    pass
```

### 错误处理策略

```python
async def safe_execute(operation: callable, *args, **kwargs) -> Result:
    """安全执行操作的包装器"""
    
    try:
        # 预检查
        if not pre_check(operation, *args, **kwargs):
            return Result.failure("Pre-check failed")
            
        # 执行操作
        result = await operation(*args, **kwargs)
        
        # 后处理
        return Result.success(result)
        
    except SecurityError as e:
        logger.error(f"Security error: {e}")
        return Result.failure(f"Security violation: {e}")
        
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        return Result.failure(f"Configuration error: {e}")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return Result.failure(f"Unexpected error: {e}")
```

## 性能优化

### 缓存机制

```python
class CacheManager:
    """缓存管理器"""
    
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, Any] = {}
        self.max_size = max_size
        self.access_times: Dict[str, float] = {}
        
    def get(self, key: str) -> Optional[Any]:
        """获取缓存项"""
        
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """设置缓存项"""
        
    def cleanup(self) -> None:
        """清理过期缓存"""
```

### 连接池管理

```python
class ConnectionPool:
    """HTTP连接池管理"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.connections: List[aiohttp.ClientSession] = []
        self.available_connections: asyncio.Queue = asyncio.Queue()
        
    async def get_connection(self) -> aiohttp.ClientSession:
        """获取连接"""
        
    async def release_connection(self, connection: aiohttp.ClientSession) -> None:
        """释放连接"""
```

## 测试架构

### 测试层次

1. **单元测试**: 测试单个组件功能
2. **集成测试**: 测试组件间交互
3. **端到端测试**: 测试完整用户流程
4. **性能测试**: 测试系统性能表现

### 测试工具

```python
# pytest配置
[tool.pytest]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"

# 测试固件
@pytest.fixture
def test_workspace():
    """创建测试工作区"""
    workspace = tempfile.mkdtemp()
    yield workspace
    shutil.rmtree(workspace)

@pytest.fixture
def mock_ai_response():
    """模拟AI响应"""
    return {
        'content': 'Test response',
        'tool_calls': []
    }
```

## 部署架构

### 本地部署

```python
# 本地部署脚本
def deploy_local():
    """本地部署函数"""
    
    # 1. 环境检查
    check_environment()
    
    # 2. 依赖安装
    install_dependencies()
    
    # 3. 配置初始化
    initialize_config()
    
    # 4. 工作区创建
    create_workspace()
    
    # 5. 启动服务
    start_service()
```

### 容器化部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

EXPOSE 8000
CMD ["python", "src/main.py"]
```

## 扩展性设计

### 插件系统

```python
class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        self.hooks: Dict[str, List[callable]] = {}
        
    def register_plugin(self, plugin: BasePlugin) -> None:
        """注册插件"""
        
    def execute_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """执行钩子函数"""
```

### 自定义工具开发

```python
# 自定义工具示例
class CustomTool(BaseTool):
    """自定义工具基类"""
    
    name = "custom_tool"
    description = "Custom tool description"
    
    async def execute(self, **kwargs) -> ToolResponse:
        """实现自定义逻辑"""
        
    def get_schema(self) -> Dict[str, Any]:
        """返回工具的JSON Schema"""
```

## 📈 监控和指标

### 性能监控

```python
class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        self.start_times: Dict[str, float] = {}
        
    def start_timing(self, operation: str) -> None:
        """开始计时"""
        
    def end_timing(self, operation: str) -> float:
        """结束计时"""
        
    def get_stats(self, operation: str) -> Dict[str, float]:
        """获取统计信息"""
```

### 健康检查

```python
async def health_check() -> Dict[str, Any]:
    """系统健康检查"""
    
    checks = {
        'ai_service': await check_ai_service(),
        'workspace': await check_workspace(),
        'tools': await check_tools(),
        'configuration': await check_configuration()
    }
    
    return {
        'status': 'healthy' if all(checks.values()) else 'unhealthy',
        'checks': checks,
        'timestamp': datetime.now().isoformat()
    }
```

## 🎓 最佳实践

### 代码质量

1. **类型注解**: 使用完整的类型注解
2. **文档字符串**: 为所有公共API编写文档
3. **单元测试**: 保持高测试覆盖率
4. **代码格式**: 使用black和flake8保持代码风格一致
5. **错误处理**: 实现全面的错误处理

### 性能优化

1. **异步编程**: 使用async/await提高并发性能
2. **缓存策略**: 实现智能缓存减少重复计算
3. **资源管理**: 合理管理连接和文件句柄
4. **内存优化**: 避免内存泄漏和不必要的内存占用

### 安全实践

1. **输入验证**: 验证所有外部输入
2. **最小权限**: 遵循最小权限原则
3. **安全配置**: 使用安全的默认配置
4. **日志记录**: 记录关键操作和错误信息

---

这个架构文档提供了 Suna-Lite 系统的全面技术视角，帮助开发者理解系统设计和实现细节。