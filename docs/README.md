# Suna-Lite

<div align="center">

**轻量级AI Agent系统 - 本地运行，功能强大**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.1.0-orange.svg)](https://github.com/IhyaH/suna-lite)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/IhyaH/suna-lite)
[![Contributors](https://img.shields.io/badge/Contributors-Welcome-orange.svg)](https://github.com/IhyaH/suna-lite/pulls)

**Suna-Lite** 是一个现代化的轻量级AI Agent系统，基于OpenAI API构建，集成了文件操作、命令行执行、Web搜索和浏览器自动化等核心功能。采用异步编程架构，提供安全可靠的智能助手体验。

</div>

## 主要特性

### 核心功能
- **智能对话**: 基于OpenAI GPT模型的自然语言交互
- **文件操作**: 完整的文件系统管理功能
- **命令执行**: 安全的Shell命令执行环境
- **Web搜索**: 使用Tavily API获取实时网络信息
- **浏览器自动化**: 网页交互和数据提取
- **工作区管理**: 隔离的任务执行环境

### 用户体验
- **美观界面**: 基于Rich库的彩色CLI界面
- **高度可配置**: 灵活的YAML配置系统
- **异步架构**: 高性能的异步编程模式
- **安全机制**: 多层安全防护措施
- **实时反馈**: 详细的执行状态和日志信息

## 快速开始

### 环境要求

- **Python**: 3.8+ (推荐3.11)
- **Conda**: 用于环境管理
- **网络连接**: 用于访问OpenAI API和Tavily搜索
- **操作系统**: Windows/Linux/macOS

### 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/IhyaH/suna-lite.git
cd suna-lite
```

#### 2. 创建Conda环境
```bash
# 创建Conda环境
conda create -n suna-lite python=3.11 -y

# 激活环境
# Windows:
conda activate suna-lite

# Linux/macOS:
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate suna-lite
```

#### 3. 安装依赖
```bash
# 安装项目依赖
pip install -r requirements.txt

# 开发模式安装（可选）
pip install -e .
```

#### 4. 配置系统
```bash
# 复制配置文件模板（如果需要）
cp config.yaml.example config.yaml

# 编辑config.yaml文件，配置必要的API密钥
# 项目现在使用YAML配置文件，无需.env文件
```

#### 5. 运行程序
```bash
# 激活环境（如果还没有激活）
conda activate suna-lite

# 启动程序
python src/main.py

# 或者使用启动脚本
python run.py
```

### 基本使用

启动程序后，您将看到一个美观的命令行界面：

```
╔═══════════════════════════════════════════════════════════════╗
║                    Suna-Lite v0.1.0                          ║
║              简化版AI Agent系统 - 本地运行                        ║
║                    作者: Suna-Lite Team                      ║
╚═══════════════════════════════════════════════════════════════╝

**AI Agent**: 基于 OpenAI API 的智能对话助手
**文件操作**: 读写文件、目录管理
**命令执行**: 在安全环境中运行系统命令
**Web搜索**: 使用Tavily API获取最新信息
**浏览器自动化**: 网页交互和数据提取
**工作区管理**: 隔离的任务环境

## 可用命令

- `/help` - 显示此帮助信息
- `/clear` - 清空对话历史
- `/reset` - 重置Agent状态
- `/workspace` - 显示工作区信息
- `/config` - 显示当前配置
- `/exit` - 退出程序

你: 请创建一个名为hello.txt的文件，内容为'Hello World!'
```

## 项目结构

```
suna-lite/
├── src/                          # 主要源代码
│   ├── agent/                    # AI Agent核心
│   │   ├── agent.py              # 主Agent类
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
├── docs/                         # 项目文档
│   ├── README.md                 # 主文档
│   ├── guides/                   # 用户指南
│   ├── reference/                # 参考资料
│   ├── development/             # 开发文档
│   ├── INSTALLATION.md           # 安装指南
│   ├── USAGE.md                  # 使用说明
│   ├── CONFIGURATION.md          # 配置说明
│   ├── EXAMPLES.md               # 使用示例
│   └── ARCHITECTURE.md           # 架构文档
├── scripts/                      # 实用脚本
├── config.yaml                   # 配置文件
├── requirements.txt              # Python依赖
├── setup.py                      # 安装脚本
└── run.py                        # 快速启动脚本
```

## 详细文档

### 用户指南
- [安装指南](guides/INSTALLATION.md) - 详细的安装步骤和配置说明
- [使用说明](USAGE.md) - 完整的使用指南和功能介绍
- [配置指南](guides/CONFIG_GUIDE.md) - 详细的配置说明
- [使用示例](EXAMPLES.md) - 实际使用案例和最佳实践

### 参考资料
- [项目结构](reference/PROJECT_STRUCTURE.md) - 完整的项目结构说明
- [架构文档](ARCHITECTURE.md) - 系统架构设计说明
- [开发者指南](reference/CLAUDE.md) - 开发者指南和开发规范

### 开发文档
- [贡献指南](../CONTRIBUTING.md) - 如何参与项目开发
- [许可证](../LICENSE) - 项目许可证信息

## 功能模块

### AI Agent核心
- 基于OpenAI GPT模型的智能对话
- 工具调用和决策支持
- 对话历史管理
- 多轮对话上下文维护

### 文件操作工具
- 文件和目录的创建、读取、写入、删除
- 文件搜索和内容提取
- 文件信息查询
- 批量文件操作

### 命令行工具
- 安全的Shell命令执行
- 工作目录管理
- 命令输出捕获
- 超时控制和错误处理

### Web搜索工具
- 使用Tavily API进行网络搜索
- 网页内容获取和解析
- 结构化数据提取
- 搜索结果分析和整理

### 浏览器自动化
- 网页导航和交互
- 表单填写和提交
- 元素定位和操作
- 页面内容提取

### 工作区管理
- 隔离的执行环境
- 会话状态管理
- 文件系统隔离
- 自动清理机制

## 配置说明

### YAML配置文件

在 `config.yaml` 中可以进行更详细的配置：

```yaml
# config.yaml - 主配置文件
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
```

## 安全特性

- **路径安全**: 防止路径遍历攻击
- **命令过滤**: 阻止危险的系统命令
- **沙箱环境**: 隔离的工作区执行环境
- **权限控制**: 限制文件系统访问范围
- **输入验证**: 严格参数验证和清理

## 使用示例

### 文件操作
```bash
你: 请创建一个Python脚本，计算斐波那契数列的前20项
Suna: [创建fibonacci.py文件，包含完整的Python代码]

你: 分析当前目录下的所有Python文件
Suna: [扫描并分析所有.py文件，生成详细报告]
```

### Web搜索
```bash
你: 搜索最新的AI发展趋势
Suna: [执行网络搜索，返回最新的AI发展动态]

你: 查找Python异步编程的最佳实践
Suna: [搜索并整理相关资料，提供实用建议]
```

### 系统命令
```bash
你: 查看当前目录的文件列表
Suna: [执行ls命令，显示文件列表]

你: 检查系统资源使用情况
Suna: [执行系统监控命令，提供资源使用分析]
```

### 数据分析
```bash
你: 分析当前工作区的文件类型分布
Suna: [分析文件类型，生成统计报告]

你: 批量处理CSV文件并生成图表
Suna: [使用pandas处理数据，创建可视化图表]
```

### 浏览器自动化
```bash
你: 打开百度首页并搜索"人工智能"
Suna: [启动浏览器，执行搜索操作]

你: 抓取网页数据并保存到文件
Suna: [访问指定网页，提取数据并保存]
```

## 贡献指南

我们欢迎所有形式的贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目开发。

### 开发环境设置

1. Fork 项目
2. 创建功能分支: `git checkout -b feature/AmazingFeature`
3. 提交更改: `git commit -m 'Add some AmazingFeature'`
4. 推送到分支: `git push origin feature/AmazingFeature`
5. 打开Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 致谢

### 原创项目
- [Suna](https://github.com/kortix-ai/suna) by [kortix-ai](https://github.com/kortix-ai) - 本项目起源于Suna，感谢其优秀的架构设计和实现

### 核心技术
- [OpenAI](https://openai.com/) - 提供强大的AI模型
- [Rich](https://github.com/Textualize/rich) - 美观的终端界面库
- [Click](https://click.palletsprojects.com/) - 优雅的命令行界面框架
- [Selenium](https://www.selenium.dev/) - 浏览器自动化工具

## 联系我们

- 项目主页: [https://github.com/IhyaH/suna-lite](https://github.com/IhyaH/suna-lite)
- 问题反馈: [GitHub Issues](https://github.com/IhyaH/suna-lite/issues)
- 邮箱: contact@suna-lite.com

---

<div align="center">

**让AI助手成为您的得力伙伴！**

[返回顶部](#suna-lite-)

</div>