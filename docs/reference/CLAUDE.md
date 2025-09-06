# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Suna-Lite 是一个轻量级的AI代理系统，基于OpenAI API构建，提供了文件操作、命令行执行、Web搜索和浏览器自动化等核心功能。该项目采用模块化设计，使用Python异步编程模式，具有完善的工具系统和安全机制。

### 主要特性
- 🧠 **智能对话**: 基于OpenAI GPT模型的自然语言交互
- 📁 **文件操作**: 完整的文件系统管理功能
- 🖥️ **命令执行**: 安全的Shell命令执行环境
- 🌐 **Web搜索**: 实时网络信息获取（使用Tavily API）
- 🌍 **浏览器自动化**: 网页交互和数据提取
- 📝 **工作区管理**: 隔离的任务执行环境
- 🎨 **美观界面**: 基于Rich库的彩色CLI界面
- 🔧 **高度可配置**: 灵活的YAML配置系统

### 技术架构
- **异步编程**: 使用 `async/await` 提高并发性能
- **模块化设计**: 工具系统可扩展，支持动态注册
- **安全机制**: 路径隔离、命令过滤、沙箱环境
- **配置管理**: 简化的YAML配置系统，无需环境变量文件

## 常用命令

### 环境管理 (使用Conda)
```bash
# 创建Conda环境
conda create -n suna-lite python=3.11 -y

# 激活环境
# Windows:
conda activate suna-lite
# Linux/macOS:
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate suna-lite

# 安装依赖
pip install -r requirements.txt

# 开发模式安装
pip install -e .
```

### 运行项目
```bash
# 直接运行主程序
python src/main.py

# 使用启动脚本
python run.py

# 使用配置文件
python src/main.py --config config.yaml

# 调试模式
python src/main.py --debug

# 显示版本
python src/main.py --version
```

### 测试和验证
```bash
# 运行功能测试
python tests/test_functionality.py

# 运行工具测试
python tests/test_tools.py

# 运行对话测试
python tests/test_conversation.py

# 运行所有工具测试
python tests/test_all_tools.py

# 分析配置文件
python scripts/config_analysis.py
```

## 项目结构

```
suna-lite/
├── src/                          # 主要源代码
│   ├── agent/                    # AI代理核心
│   │   ├── agent.py              # 主代理类
│   │   ├── prompts.py            # 系统提示词
│   │   └── tools/                # 工具模块
│   │       ├── base_tool.py      # 工具基类
│   │       ├── file_tool.py      # 文件操作工具
│   │       ├── shell_tool.py     # Shell命令工具
│   │       ├── web_tool.py       # Web搜索工具
│   │       ├── tavily_tool.py    # Tavily搜索工具
│   │       └── browser_tool.py   # 浏览器自动化工具
│   ├── config/                   # 配置管理
│   │   ├── settings.py           # 配置设置类
│   │   └── env_loader.py         # 环境变量加载
│   ├── utils/                    # 工具类
│   │   ├── logger.py             # 日志系统
│   │   └── helpers.py            # 辅助函数
│   ├── workspace/                # 工作区管理
│   │   └── manager.py            # 工作区管理器
│   └── main.py                   # 主入口点
├── tests/                        # 测试文件
├── docs/                         # 文档
├── scripts/                      # 实用脚本
├── config.yaml                   # 配置文件
├── requirements.txt              # Python依赖
├── setup.py                      # 安装脚本
└── run.py                        # 快速启动脚本
```

## 核心架构

### 1. AI代理核心 (SunaAgent)
- **位置**: `src/agent/agent.py`
- **功能**: 
  - 与OpenAI API交互
  - 工具调用和决策支持
  - 对话历史管理
  - 多轮对话上下文维护

### 2. 工具系统
- **基类**: `src/agent/tools/base_tool.py`
- **工具注册表**: 管理所有可用工具
- **主要工具**:
  - **文件工具**: 读写文件、目录管理、搜索功能
  - **Shell工具**: 安全的命令执行环境
  - **Web工具**: 网络搜索和内容获取
  - **浏览器工具**: 网页交互和数据提取

### 3. 工作区管理
- **位置**: `src/workspace/manager.py`
- **功能**:
  - 隔离的文件操作环境
  - 会话级别的文件管理
  - 安全路径验证
  - 自动清理机制

### 4. 配置系统
- **配置类**: `src/config/settings.py`
- **加载优先级**: YAML文件 > 默认值
- **配置验证**: 自动验证配置有效性
- **主要配置项**:
  - AI模型配置 (API密钥、模型名称、参数)
  - 工作区配置 (路径、大小限制)
  - 工具开关配置
  - 日志配置

## 配置系统

### 配置文件结构
```yaml
# config.yaml
agent:
  model: "Qwen/Qwen3-Coder-480B-A35B-Instruct"
  base_url: "https://newapi.ihyah.top:12321/v1"
  api_key: "your_api_key_here"
  max_tokens: 4000
  temperature: 0.7
  max_conversation_history: 10

workspace:
  path: "./workspace"
  max_size_mb: 100
  auto_cleanup: true

tools:
  file_operations: true
  shell_commands: true
  web_search: true
  browser_automation: true

logging:
  level: "INFO"
  file: "./suna-lite.log"
```

### 配置管理
- **配置类**: `src/config/settings.py`
- **加载优先级**: YAML文件 > 默认值
- **配置验证**: 自动验证配置有效性
- **主要配置项**:
  - AI模型配置 (API密钥、模型名称、参数)
  - 工作区配置 (路径、大小限制)
  - 工具开关配置
  - 日志配置

### 依赖管理

主要依赖包括：
- `openai>=1.0.0` - OpenAI API集成
- `click>=8.0.0` - 命令行界面框架
- `rich>=13.0.0` - 美观的终端UI
- `selenium>=4.15.0` - 浏览器自动化
- `beautifulsoup4>=4.12.0` - HTML解析
- `pyyaml>=6.0.0` - YAML配置文件处理
- `python-dotenv>=1.0.0` - 环境变量管理
- `tavily-python>=0.5.0` - 搜索API集成

## 关键技术特点

### 1. 异步编程模式
- 使用 `async/await` 进行异步处理
- 支持并发工具执行
- 提高系统响应性能

### 2. 安全机制
- **路径安全**: 防止路径遍历攻击
- **命令过滤**: 阻止危险的系统命令
- **沙箱环境**: 隔离的工作区执行环境
- **权限控制**: 限制文件系统访问范围

### 3. 模块化设计
- 工具系统可扩展
- 配置系统灵活
- 日志系统完善
- 错误处理机制健全

### 4. 用户体验
- 基于Rich库的美观CLI界面
- 实时进度显示
- 详细的帮助信息
- 对话历史管理

## 开发注意事项

### 代码结构
- 所有工具都继承自 `BaseTool` 基类，确保统一的接口
- 使用异步编程模式处理IO密集型操作
- 配置通过 `config.yaml` 集中管理，支持环境变量覆盖
- 日志系统使用 `utils.logger` 模块，支持不同级别输出

### 安全特性
- 文件操作限制在工作区内，防止路径遍历攻击
- Shell命令执行包含黑名单过滤，阻止危险操作
- 浏览器自动化支持无头模式，可在安全环境中运行
- 网络访问可通过配置文件限制域名

### 扩展开发
- 新工具应放置在 `src/agent/tools/` 目录下
- 继承 `BaseTool` 类并实现必要的方法
- 在 `config.yaml` 中添加相应的开关配置
- 更新 `agent.py` 中的工具注册逻辑

## 开发工作流程

### 1. 添加新工具
```python
# 1. 继承BaseTool类
class CustomTool(BaseTool):
    def __init__(self):
        super().__init__("custom_tool", "自定义工具描述")
    
    async def execute(self, **kwargs) -> ToolResponse:
        # 实现工具逻辑
        return ToolResponse(success=True, message="执行成功")
    
    def get_schema(self) -> Dict[str, Any]:
        # 返回工具的JSON Schema
        return {
            "type": "function",
            "function": {
                "name": "custom_tool",
                "description": "自定义工具描述",
                "parameters": {}
            }
        }

# 2. 在agent.py中注册工具
if self.settings.tools.custom_tool_enabled:
    custom_tool = CustomTool()
    self.tool_registry.register(custom_tool)
```

### 2. 修改配置
```python
# 1. 在settings.py中添加新的配置项
@dataclass
class CustomConfig:
    custom_setting: str = "default_value"

# 2. 在Settings类中集成
@dataclass
class Settings:
    custom: CustomConfig = field(default_factory=CustomConfig)
```

### 3. 测试开发
```python
# 创建测试文件
async def test_custom_functionality():
    # 测试逻辑
    assert result.success == True
    assert "expected" in result.message
```

## 环境配置

### 配置文件管理
项目现在使用简化的配置系统：
- **主配置文件**: `config.yaml` - 包含所有配置项
- **环境变量**: 通过 `env_loader.py` 加载（保留用于兼容性）
- **配置优先级**: YAML文件 > 默认值

### 当前配置状态
项目已移除 `.env` 文件依赖，所有配置通过 `config.yaml` 管理：

**配置步骤**：
1. 复制 `config.yaml` 文件（如果不存在）
2. 编辑 `config.yaml` 文件，配置必要的API密钥
3. 运行项目，配置会自动加载

**config.yaml 示例配置**：
```yaml
# config.yaml
agent:
  model: "Qwen/Qwen3-Coder-480B-A35B-Instruct"
  base_url: "https://newapi.ihyah.top:12321/v1"
  api_key: "your_api_key_here"
  max_tokens: 4000
  temperature: 0.7
  
search:
  engine: "tavily"
  max_results: 10
  timeout_seconds: 15
  api_key: "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"
  
workspace:
  path: "./workspace"
  max_size_mb: 100
  auto_cleanup: true
```

## 常见问题和解决方案

### 1. 配置问题
- **问题**: API密钥配置错误
- **解决**: 检查 `config.yaml` 中的 `api_key` 和 `base_url` 配置
- **注意**: 项目现在只使用 YAML 配置文件，确保 `config.yaml` 文件存在且格式正确

### 2. 权限问题
- **问题**: 工作区权限不足
- **解决**: 确保工作区目录有读写权限

### 3. 网络问题
- **问题**: API连接失败
- **解决**: 检查网络连接和API服务状态

### 4. 依赖问题
- **问题**: Python包依赖冲突
- **解决**: 使用conda创建独立环境

## 性能优化建议

### 1. 异步优化
- 使用异步IO操作
- 避免阻塞调用
- 合理设置超时时间

### 2. 内存管理
- 定期清理工作区
- 限制文件大小
- 监控内存使用

### 3. 缓存策略
- 缓存常用数据
- 避免重复计算
- 使用LRU缓存机制

## 调试和日志

### 日志级别
- **DEBUG**: 详细调试信息
- **INFO**: 一般信息 (默认)
- **WARNING**: 警告信息
- **ERROR**: 错误信息
- **CRITICAL**: 严重错误

### 调试技巧
```bash
# 启用调试模式
python src/main.py --debug

# 查看日志文件
tail -f suna-lite.log

# 检查配置
python scripts/config_analysis.py
```

## 测试和调试

### 测试系统
项目包含完整的测试套件：
- **功能测试**: `tests/test_functionality.py` - 验证基本模块功能
- **工具测试**: `tests/test_tools.py` - 测试所有工具功能
- **对话测试**: `tests/test_conversation.py` - 测试AI代理对话能力
- **综合测试**: `tests/test_all_tools.py` - 全面测试所有工具

### 调试工具
- 使用 `python -m pdb` 进行交互式调试
- 日志文件默认为 `./suna-lite.log`
- 工作区默认路径为 `./workspace`
- 配置分析工具: `python scripts/config_analysis.py`
- 支持实时配置重载和状态重置

### 测试命令
```bash
# 运行所有测试
python tests/test_functionality.py
python tests/test_tools.py
python tests/test_conversation.py

# 单独测试特定工具
python tests/test_all_tools.py
```

## 部署注意事项

### 1. 环境要求
- Python 3.8+
- 网络连接 (API访问)
- 足够的磁盘空间 (工作区)

### 2. 安全考虑
- 保护API密钥
- 限制文件访问权限
- 定期更新依赖包

### 3. 监控建议
- 监控API使用量
- 跟踪错误日志
- 定期检查工作区大小

## 扩展开发

### 1. 插件系统
- 基于BaseTool的插件架构
- 动态工具注册
- 配置驱动的功能开关

### 2. API扩展
- 支持多种LLM提供商
- 自定义工具开发
- 第三方服务集成

### 3. 界面扩展
- Web界面支持
- GUI应用开发
- 移动端适配

---

## 项目当前状态

### 已完成的功能
- ✅ **配置系统简化**: 移除 `.env` 文件依赖，使用纯 YAML 配置
- ✅ **Tavily 搜索集成**: 完整的 Tavily API 工具集（6个功能）
- ✅ **工具测试系统**: 完整的测试套件覆盖所有核心功能
- ✅ **项目结构重组**: 统一的测试和脚本目录结构
- ✅ **模块导入修复**: 所有路径问题已解决
- ✅ **编码兼容性**: 移除emoji字符，支持Windows gbk编码

### 核心工具状态
- ✅ **文件工具**: 读写、列表、删除功能正常
- ✅ **Shell工具**: 安全命令执行功能正常
- ✅ **Web工具**: Tavily搜索功能正常
- ✅ **浏览器工具**: 基本功能正常
- ✅ **AI代理**: 对话和工具调用功能正常

### 开发环境
- **Python**: 3.11+ (推荐使用conda)
- **主要依赖**: openai, tavily-python, selenium, rich
- **配置文件**: `config.yaml` (单一配置源)
- **测试覆盖**: 4个测试文件，覆盖所有核心功能

**重要提示**: 
- 始终在激活的conda环境中工作
- 定期备份配置文件
- 遵循安全最佳实践
- 保持代码风格一致性
- 用户是编程学习者，请提供详细的注释和解释