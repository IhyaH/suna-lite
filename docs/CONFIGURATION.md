# Suna-Lite 配置指南

本文档详细说明 Suna-Lite 的配置系统，包括配置文件的使用、配置选项和最佳实践。

## 配置系统概述

Suna-Lite 使用简化的 YAML 配置系统，配置文件按以下优先级加载：

1. **YAML配置文件** (`config.yaml`)
2. **默认配置** (代码中的默认值)

## 配置文件结构

### 主要配置文件 (`config.yaml`)

这是项目的主要配置文件，包含所有必要的配置选项：

```yaml
# AI Agent配置
agent:
  model: "your_model_here"
  base_url: "your_api_base_url_here"
  api_key: "your_api_key_here"
  max_tokens: 4000
  temperature: 0.7
  max_conversation_history: 10

# 搜索配置
search:
  engine: "tavily"
  max_results: 10
  timeout_seconds: 15
  api_key: "your_tavily_api_key_here"

# 工作区配置
workspace:
  path: "./workspace"
  max_size_mb: 100
  auto_cleanup: true

# 浏览器配置
browser:
  headless: true
  timeout_seconds: 30
  window_size:
    width: 1920
    height: 1080

# 工具开关
tools:
  file_operations: true
  shell_commands: true
  web_search: true
  browser_automation: true

# 日志配置
logging:
  level: "INFO"
  file: "./suna-lite.log"
  max_size_mb: 10
  backup_count: 5

# 安全配置
security:
  allow_network: true
  allowed_domains: []
  block_shell_commands: ["rm -rf", "format", "del"]
```

## 配置加载机制

### 加载顺序

1. **首先加载默认配置** (代码中的硬编码值)
2. **然后加载YAML配置文件** (如果存在)

### 配置优先级

YAML配置文件会覆盖默认配置。系统会自动合并配置，缺失的配置项会使用默认值。

### 配置验证

程序启动时会自动验证配置的有效性，确保所有必需的配置项都存在且格式正确。

## 必需配置项

### AI Agent配置

以下配置项是必需的：

```yaml
# AI Agent配置
agent:
  model: "your_model_here"  # 模型名称
  base_url: "your_api_base_url_here"   # API基础URL
  api_key: "your_api_key_here"                   # API密钥
  max_tokens: 4000                               # 最大令牌数
  temperature: 0.7                               # 温度参数
```

### 搜索配置

```yaml
# 搜索配置
search:
  engine: "tavily"                                # 搜索引擎
  api_key: "your_tavily_api_key_here"            # Tavily API密钥
```

### 配置验证

程序启动时会自动验证以下配置：

- ✅ AI AgentAPI密钥存在且有效
- ✅ Base URL 格式正确
- ✅ 最大令牌数 > 0
- ✅ 温度参数在 0-2 之间
- ✅ 工作区路径可访问
- ✅ 搜索API密钥配置正确

## 配置示例

### 基础配置 (config.yaml)

```yaml
# 基础AI Agent配置
agent:
  model: "your_model_here"
  base_url: "your_api_base_url_here"
  api_key: "your_api_key_here"
  max_tokens: 4000
  temperature: 0.7

# 基础搜索配置
search:
  engine: "tavily"
  max_results: 10
  api_key: "your_tavily_api_key_here"

# 基础工作区配置
workspace:
  path: "./workspace"
  max_size_mb: 100
  auto_cleanup: true

# 基础日志配置
logging:
  level: "INFO"
  file: "./suna-lite.log"
```

### 高级配置 (config.yaml)

```yaml
# 高级AI Agent配置
agent:
  model: "your_model_here"
  base_url: "your_api_base_url_here"
  api_key: "your_api_key_here"
  max_tokens: 8000
  temperature: 0.3
  max_conversation_history: 20

# 高级搜索配置
search:
  engine: "tavily"
  max_results: 20
  timeout_seconds: 30
  api_key: "your_tavily_api_key_here"

# 大工作区配置
workspace:
  path: "./large_workspace"
  max_size_mb: 1000
  auto_cleanup: true

# 浏览器详细配置
browser:
  headless: false
  timeout_seconds: 60
  window_size:
    width: 2560
    height: 1440

# 工具详细配置
tools:
  file_operations: true
  shell_commands: true
  web_search: true
  browser_automation: false

# 安全配置
security:
  allow_network: true
  allowed_domains: ["*.example.com"]
  block_shell_commands: ["rm -rf", "format", "del", "shutdown"]
```

## 配置验证和调试

### 验证配置

使用 `/config` 命令查看当前配置：

```
你: /config
Suna: [显示当前配置信息]
```

### 调试配置问题

如果遇到配置问题，可以：

1. **检查 `config.yaml` 文件** 是否存在并正确配置
2. **验证YAML语法** 是否正确
3. **查看日志文件** 中的错误信息
4. **使用调试模式** 启动程序：

```bash
python src/main.py --debug
```

### 常见配置问题

#### 1. API密钥错误

```
错误：缺少AI AgentAPI密钥
```

**解决方案**：
- 检查 `config.yaml` 文件中的 `agent.api_key` 配置
- 确保API密钥格式正确

#### 2. 网络连接问题

```
错误：无法连接到API服务
```

**解决方案**：
- 检查 `agent.base_url` 配置
- 确保网络连接正常
- 验证API服务可用性

#### 3. 工作区权限问题

```
错误：无法创建工作区目录
```

**解决方案**：
- 检查 `workspace.path` 配置
- 确保有目录创建权限
- 手动创建工作区目录

#### 4. 搜索API配置问题

```
错误：搜索功能不可用
```

**解决方案**：
- 检查 `search.api_key` 配置
- 确保Tavily API密钥正确

## 配置最佳实践

### 1. 安全性

- **不要提交敏感信息** 到版本控制系统
- 使用 `config.yaml` 文件存储配置，但不要将包含API密钥的版本提交到代码库
- 使用配置模板文件，让用户自行填写敏感信息
- 定期轮换API密钥

### 2. 可维护性

- **使用YAML文件** 进行所有配置
- **保持配置文件结构清晰**，使用注释说明每个配置项的作用
- **分组配置相关项**，如将所有AI Agent配置放在一起
- **使用有意义的默认值**

### 3. 部署考虑

- **不同环境使用不同配置文件**
- **使用配置模板** (`config.yaml.example`)
- **自动化配置验证**
- **环境变量覆盖**（如果需要）

## 配置模板

### 开发环境 (config.dev.yaml)

```yaml
# 开发环境配置
agent:
  model: "your_model_here"
  base_url: "your_api_base_url_here"
  api_key: "dev_api_key_here"
  max_tokens: 4000
  temperature: 0.7

search:
  engine: "tavily"
  max_results: 10
  api_key: "dev_tavily_key_here"

workspace:
  path: "./dev_workspace"
  max_size_mb: 100
  auto_cleanup: true

logging:
  level: "DEBUG"
  file: "./suna-lite-dev.log"
```

### 生产环境 (config.prod.yaml)

```yaml
# 生产环境配置
agent:
  model: "your_model_here"
  base_url: "your_api_base_url_here"
  api_key: "prod_api_key_here"
  max_tokens: 8000
  temperature: 0.3

search:
  engine: "tavily"
  max_results: 20
  api_key: "prod_tavily_key_here"

workspace:
  path: "./prod_workspace"
  max_size_mb: 1000
  auto_cleanup: true

logging:
  level: "WARNING"
  file: "./suna-lite-prod.log"
  max_size_mb: 50
  backup_count: 10

security:
  allow_network: true
  allowed_domains: ["*.yourdomain.com"]
  block_shell_commands: ["rm -rf", "format", "del", "shutdown"]
```

### 测试环境 (config.test.yaml)

```yaml
# 测试环境配置
agent:
  model: "your_model_here"
  base_url: "your_api_base_url_here"
  api_key: "test_api_key_here"
  max_tokens: 1000
  temperature: 0.5

search:
  engine: "tavily"
  max_results: 5
  api_key: "test_tavily_key_here"

workspace:
  path: "./test_workspace"
  max_size_mb: 50
  auto_cleanup: true

logging:
  level: "ERROR"
  file: "./suna-lite-test.log"

tools:
  browser_automation: false  # 测试环境禁用浏览器自动化
```

## 配置文件示例模板 (config.yaml.example)

```yaml
# Suna-Lite 配置文件示例
# 复制此文件为 config.yaml 并填写您的实际配置

# AI Agent配置
agent:
  model: "your_model_here"
  base_url: "your_api_base_url_here"
  api_key: "your_api_key_here"
  max_tokens: 4000
  temperature: 0.7
  max_conversation_history: 10

# 搜索配置
search:
  engine: "tavily"
  max_results: 10
  timeout_seconds: 15
  api_key: "your_tavily_api_key_here"

# 工作区配置
workspace:
  path: "./workspace"
  max_size_mb: 100
  auto_cleanup: true

# 浏览器配置
browser:
  headless: true
  timeout_seconds: 30
  window_size:
    width: 1920
    height: 1080

# 工具开关
tools:
  file_operations: true
  shell_commands: true
  web_search: true
  browser_automation: true

# 日志配置
logging:
  level: "INFO"
  file: "./suna-lite.log"
  max_size_mb: 10
  backup_count: 5

# 安全配置
security:
  allow_network: true
  allowed_domains: []
  block_shell_commands: ["rm -rf", "format", "del"]
```

---

通过合理配置 Suna-Lite，您可以充分发挥其功能，同时确保安全性和可维护性。