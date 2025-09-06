# Suna-Lite

<div align="center">

**轻量级AI代理系统 - 本地运行，功能强大**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.1.0-orange.svg)](https://github.com/suna-lite/suna-lite)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/suna-lite/suna-lite)
[![Contributors](https://img.shields.io/badge/Contributors-Welcome-orange.svg)](https://github.com/suna-lite/suna-lite/pulls)

**Suna-Lite** 是一个现代化的轻量级AI代理系统，基于OpenAI API构建，集成了文件操作、命令行执行、Web搜索和浏览器自动化等核心功能。采用异步编程架构，提供安全可靠的智能助手体验。

</div>

## 快速导航

- **[完整文档](docs/README.md)** - 详细的项目文档和使用指南
- **[快速开始](docs/guides/INSTALLATION.md)** - 快速安装和配置指南
- **[项目结构](docs/reference/PROJECT_STRUCTURE.md)** - 完整的项目结构说明
- **[配置指南](docs/guides/CONFIG_GUIDE.md)** - 详细的配置说明
- **[开发指南](docs/reference/CLAUDE.md)** - 开发者指南和架构说明

## 快速开始

### 环境要求

- **Python**: 3.8+ (推荐3.11)
- **Conda**: 用于环境管理
- **网络连接**: 用于访问OpenAI API和Tavily搜索
- **操作系统**: Windows/Linux/macOS

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/suna-lite/suna-lite.git
cd suna-lite

# 2. 创建Conda环境
conda create -n suna-lite python=3.11 -y
conda activate suna-lite

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置系统
# 编辑config.yaml文件，配置必要的API密钥

# 5. 运行程序
python src/main.py
```

## 主要特性

- **智能对话**: 基于OpenAI GPT模型的自然语言交互
- **文件操作**: 完整的文件系统管理功能
- **命令执行**: 安全的Shell命令执行环境
- **Web搜索**: 使用Tavily API获取实时网络信息
- **浏览器自动化**: 网页交互和数据提取
- **工作区管理**: 隔离的任务执行环境
- **美观界面**: 基于Rich库的彩色CLI界面
- **高度可配置**: 灵活的YAML配置系统

## 项目结构

```
suna-lite/
├── src/                          # 主要源代码
├── tests/                        # 测试文件
├── docs/                         # 项目文档
│   ├── README.md                 # 主文档
│   ├── guides/                   # 用户指南
│   ├── reference/                # 参考资料
│   └── development/             # 开发文档
├── scripts/                      # 实用脚本
├── config.yaml                   # 配置文件
├── requirements.txt              # Python依赖
├── setup.py                      # 安装脚本
└── run.py                        # 快速启动脚本
```

## 贡献指南

我们欢迎所有形式的贡献！请查看 [开发指南](docs/reference/CLAUDE.md) 了解如何参与项目开发。

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系我们

- 项目主页: [https://github.com/suna-lite/suna-lite](https://github.com/suna-lite/suna-lite)
- 问题反馈: [GitHub Issues](https://github.com/suna-lite/suna-lite/issues)
- 邮箱: contact@suna-lite.com

---

<div align="center">

**让AI助手成为您的得力伙伴！**

[返回顶部](#suna-lite-)

</div>