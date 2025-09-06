# Suna-Lite 配置说明

## 配置文件结构

Suna-Lite 使用简化的YAML配置系统，优先级从高到低：

1. **YAML配置文件** (`config.yaml`) - 主要配置
2. **默认值** - 备用配置

## 主要配置文件

### 1. config.yaml (主要配置文件)

这是主要的配置文件，包含所有系统配置项：

```yaml
# AI 代理配置
agent:
  model: "Qwen/Qwen3-Coder-480B-A35B-Instruct"
  base_url: "https://newapi.ihyah.top:12321/v1"
  api_key: "your_api_key_here"
  max_tokens: 4000
  temperature: 0.7
  max_conversation_history: 10

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

# 搜索配置
search:
  engine: "tavily"
  max_results: 10
  timeout_seconds: 15
  api_key: "your_tavily_api_key_here"

# 工具配置
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

### 配置使用建议

#### 开发环境
- 使用 `config.yaml` 进行主要配置
- 根据需要调整日志级别为 DEBUG

#### 生产环境
- 在 `config.yaml` 中设置生产环境配置
- 设置适当的日志级别（WARNING 或 ERROR）
- 配置合适的工作区大小限制

## 配置验证

系统会自动验证配置的有效性，包括：
- API密钥和Base URL是否设置
- 数值类型配置是否在合理范围内
- 必要的文件路径是否存在

## 常见问题

### Q: 如何在不同的环境中使用不同的配置？
A: 可以为每个环境创建不同的YAML配置文件，如 `config.dev.yaml`、`config.prod.yaml`，然后在使用时指定配置文件路径。

### Q: API密钥安全如何保证？
A: 建议将敏感信息直接配置在 `config.yaml` 中，但不要将包含真实API密钥的配置文件提交到代码仓库。可以使用配置模板文件（如 `config.yaml.example`）作为参考。

## 切换AI模型

要切换不同的AI模型或API提供商，只需修改 `config.yaml` 中的 `agent` 部分：

```yaml
# 示例：切换到OpenAI GPT-4
agent:
  model: "gpt-4"
  base_url: "https://api.openai.com/v1"
  api_key: "your-openai-api-key"

# 示例：切换到Claude
agent:
  model: "claude-3-sonnet-20240229"
  base_url: "https://api.anthropic.com/v1"
  api_key: "your-anthropic-api-key"
```

## 配置验证

系统会自动验证配置的有效性，包括：
- API密钥和Base URL是否设置
- 数值类型配置是否在合理范围内
- 必要的文件路径是否存在

## 常见问题

### Q: 为什么修改了config.yaml但没有生效？
A: 检查 `.env` 文件中是否有覆盖配置，环境变量优先级更高。

### Q: 如何在不同的环境中使用不同的配置？
A: 可以为每个环境创建不同的配置文件，然后通过符号链接或环境变量指定。

### Q: API密钥安全如何保证？
A: 建议将敏感信息放在环境变量中，而不是提交到代码仓库的配置文件中。