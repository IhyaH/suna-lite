# Suna-Lite 安装指南

本指南将帮助您在本地环境中安装和配置 Suna-Lite。

## 系统要求

### 必需条件
- **Python**: 3.8 或更高版本
- **操作系统**: Windows, macOS, 或 Linux
- **网络连接**: 用于访问 OpenAI API
- **内存**: 至少 512MB 可用内存
- **存储**: 至少 100MB 可用空间

### 推荐配置
- **Python**: 3.9+ (推荐 3.11)
- **内存**: 1GB 或更多
- **存储**: 1GB 或更多 (用于工作区和日志)

## 安装步骤

### 步骤 1: 获取源代码

#### 方法 A: 克隆 GitHub 仓库 (推荐)

```bash
# 克隆项目
git clone https://github.com/IhyaH/suna-lite.git

# 进入项目目录
cd suna-lite
```

#### 方法 B: 下载压缩包

1. 访问 [GitHub Releases](https://github.com/IhyaH/suna-lite/releases)
2. 下载最新版本的源代码压缩包
3. 解压到您选择的目录
4. 进入解压后的目录

### 步骤 2: 环境准备

#### 创建Conda环境 (强烈推荐)

```bash
# 创建Conda环境
conda create -n suna-lite python=3.11 -y

# 激活Conda环境

# Windows:
conda activate suna-lite

# macOS/Linux:
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate suna-lite
```

#### 验证 Python 版本

```bash
python --version
# 应该显示 Python 3.8 或更高版本
```

### 步骤 3: 安装依赖

#### 使用 pip 安装

```bash
# 升级 pip 到最新版本
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

#### 依赖包说明

主要依赖包包括：

- **openai**: OpenAI API 客户端
- **click**: 命令行界面框架
- **rich**: 美观的终端输出
- **pyyaml**: YAML 配置文件解析
- **beautifulsoup4**: HTML 解析
- **requests**: HTTP 请求库
- **selenium**: 浏览器自动化 (可选)
- **tavily-python**: Tavily 搜索 API 客户端

### 步骤 4: 配置系统

#### 编辑 YAML 配置文件

项目现在使用简化的 YAML 配置系统，无需环境变量文件：

```bash
# 编辑主配置文件
# Windows: 使用记事本或其他编辑器
# macOS/Linux: 使用 nano 或 vim
nano config.yaml
```

#### 配置 API 密钥

编辑 `config.yaml` 文件，至少配置以下必需项：

```yaml
# AI 代理配置
agent:
  model: "Qwen/Qwen3-Coder-480B-A35B-Instruct"
  base_url: "https://newapi.ihyah.top:12321/v1"
  api_key: "your_api_key_here"
  max_tokens: 4000
  temperature: 0.7

# 搜索配置
search:
  engine: "tavily"
  api_key: "your_tavily_api_key_here"

# 工作区配置
workspace:
  path: "./workspace"
  max_size_mb: 100
  auto_cleanup: true
```

**重要**: 请将 `your_api_key_here` 和 `your_tavily_api_key_here` 替换为您的实际 API 密钥。

### 步骤 5: 验证安装

#### 运行测试脚本

```bash
# 运行简单的测试
python -c "import src; print('[成功] 导入成功')"

# 测试配置加载
python -c "from src.config.settings import Settings; print('[成功] 配置系统正常')"

# 运行功能测试
python tests/test_functionality.py
```

#### 首次运行

安装完成后，您可以通过以下步骤启动Suna-Lite：

```bash
# 确保Conda环境已激活
conda activate suna-lite

# 启动Suna-Lite
python src/main.py
```

如果看到欢迎界面，说明安装成功！

#### 启动成功界面

```
╔═══════════════════════════════════════════════════════════════╗
║                    Suna-Lite v0.1.0                          ║
║              简化版AI代理系统 - 本地运行                        ║
║                    作者: Suna-Lite Team                      ║
╚═══════════════════════════════════════════════════════════════╝

**AI代理**: 基于 OpenAI API 的智能对话助手
**文件操作**: 读写文件、目录管理
**命令执行**: 在安全环境中运行系统命令
**Web搜索**: 使用Tavily API获取最新信息
**浏览器自动化**: 网页交互和数据提取
**工作区管理**: 隔离的任务环境

## 可用命令

- `/help` - 显示此帮助信息
- `/clear` - 清空对话历史
- `/reset` - 重置代理状态
- `/workspace` - 显示工作区信息
- `/config` - 显示当前配置
- `/exit` - 退出程序

你:
```

## 高级配置

### YAML 配置文件详细说明

对于更复杂的配置，您可以编辑 `config.yaml` 文件：

```yaml
# config.yaml - 完整配置示例
# AI 代理配置
agent:
  model: "Qwen/Qwen3-Coder-480B-A35B-Instruct"
  base_url: "https://newapi.ihyah.top:12321/v1"
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

### 浏览器自动化配置

如果您想使用浏览器自动化功能，需要额外安装 Chrome 浏览器和 ChromeDriver：

#### Windows

1. 下载并安装 [Chrome 浏览器](https://www.google.com/chrome/)
2. 下载对应版本的 [ChromeDriver](https://chromedriver.chromium.org/)
3. 将 ChromeDriver 添加到系统 PATH

#### macOS

```bash
# 使用 Homebrew 安装 Chrome
brew install --cask google-chrome

# 安装 ChromeDriver
brew install chromedriver
```

#### Linux (Ubuntu/Debian)

```bash
# 安装 Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install google-chrome-stable

# 安装 ChromeDriver
apt-get install chromium-chromedriver
```

## 故障排除

### 常见问题

#### 1. Python 版本不兼容

**错误**: `TypeError: 'type' object is not subscriptable`

**解决**: 升级到 Python 3.9+

```bash
# 检查 Python 版本
python --version

# 如果版本低于 3.9，请升级 Python
```

#### 2. 依赖安装失败

**错误**: `Could not find a version that satisfies the requirement...`

**解决**: 尝试以下方法

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 或者使用 conda
conda install -c conda-forge --file requirements.txt
```

#### 3. OpenAI API 连接失败

**错误**: `ConnectionError` 或 `AuthenticationError`

**解决**: 检查网络连接和 API 密钥

```bash
# 检查网络连接
ping openai.com

# 验证 API 密钥
curl -H "Authorization: Bearer your_api_key" https://api.openai.com/v1/models
```

#### 4. 浏览器自动化失败

**错误**: `WebDriverException` 或 `SessionNotCreatedException`

**解决**: 检查 Chrome 和 ChromeDriver 版本匹配

```bash
# 检查 Chrome 版本
google-chrome --version

# 检查 ChromeDriver 版本
chromedriver --version

# 确保版本匹配
```

#### 5. 权限问题

**错误**: `PermissionError` 或 `Access denied`

**解决**: 检查文件权限

```bash
# macOS/Linux
chmod +x run.py

# Windows
# 以管理员身份运行命令提示符
```

### 日志调试

启用详细日志来诊断问题：

```bash
# 修改配置文件设置调试级别
# 在 config.yaml 中设置：
# logging:
#   level: "DEBUG"

# 运行并查看日志
python src/main.py --debug
```

### 运行测试验证安装

```bash
# 运行功能测试
python tests/test_functionality.py

# 运行工具测试
python tests/test_tools.py

# 运行对话测试
python tests/test_conversation.py
```

## 开发环境设置

如果您想参与开发，请按以下步骤设置开发环境：

### 安装开发依赖

```bash
# 安装开发工具
pip install pytest pytest-asyncio black flake8 mypy

# 安装预提交钩子 (可选)
pip install pre-commit
pre-commit install
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_functionality.py

# 运行覆盖率测试
pytest --cov=src
```

### 代码格式化

```bash
# 格式化代码
black src/

# 检查代码风格
flake8 src/

# 类型检查
mypy src/
```

## 下一步

安装完成后，您可以：

1. 阅读 [使用说明](USAGE.md) 了解如何使用 Suna-Lite
2. 查看 [架构文档](ARCHITECTURE.md) 了解系统设计
3. 浏览 [使用示例](EXAMPLES.md) 学习实际用法
4. 加入我们的社区讨论和贡献

## 获取帮助

如果安装过程中遇到问题：

1. 查看 [故障排除](#故障排除) 部分
2. 搜索 [GitHub Issues](https://github.com/IhyaH/suna-lite/issues)
3. 创建新的 Issue 描述您的问题
4. 发送邮件至 support@suna-lite.com

---

祝您使用愉快！