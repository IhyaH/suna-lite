# Suna-Lite 使用说明

本指南详细介绍 Suna-Lite 的功能特性和使用方法。

## 核心概念

### AI Agent
Suna-Lite 的核心是一个智能 AI Agent，它可以：
- 理解自然语言指令
- 选择合适的工具执行任务
- 提供清晰的执行结果
- 维护对话上下文

### 工具系统
AI Agent通过各种工具与环境交互：
- **文件工具**: 管理文件和目录
- **Shell工具**: 执行系统命令
- **Web工具**: 搜索和获取网页内容
- **浏览器工具**: 自动化网页操作

### 工作区
每个会话都在独立的工作区中进行：
- 隔离的文件系统环境
- 会话状态管理
- 自动清理机制

## 基本使用

### 启动程序

在启动 Suna-Lite 之前，请确保已经按照 [安装指南](INSTALLATION.md) 完成了环境配置。

#### 手动启动步骤

**1. 激活Conda环境**
```bash
# Windows
conda activate suna-lite

# Linux/macOS
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate suna-lite
```

**2. 启动程序**
```bash
# Windows
python src/main.py

# Linux/macOS
python3 src/main.py
```

#### 日常使用

对于日常使用，只需要确保Conda环境已激活，然后运行主程序：

```bash
# 激活环境（如果还未激活）
conda activate suna-lite

# 启动Suna-Lite
python src/main.py
```

启动后您会看到：

```
╔═══════════════════════════════════════════════════════════════╗
║                    Suna-Lite v0.1.0                          ║
║              简化版AIAgent系统 - 本地运行                        ║
║                    作者: Suna-Lite Team                      ║
╚═══════════════════════════════════════════════════════════════╝
```

### 基本对话

```
你: 你好！
Suna: 你好！我是 Suna-Lite，一个AI助手。我可以帮助您进行文件操作、执行命令、搜索网络和自动化网页操作。有什么我可以帮助您的吗？
```

### 查看帮助

```
你: /help
Suna: [显示详细的帮助信息]
```

## 文件操作

### 基本文件操作

#### 创建文件
```
你: 创建一个名为 notes.txt 的文件，内容为 "今天学习了 AI 助手的使用"
Suna: ✓ 创建文件成功: notes.txt
```

#### 读取文件
```
你: 读取 notes.txt 文件的内容
Suna: ✓ 读取文件成功: notes.txt
    今天学习了 AI 助手的使用
```

#### 列出目录
```
你: 列出当前目录的所有文件
Suna: ✓ 列出目录成功: . (5 项)
    文件: notes.txt (24 字节)
    文件: config.yaml (1.2 KB)
    目录: docs/
    文件: run.py (2.1 KB)
    文件: requirements.txt (456 字节)
```

### 高级文件操作

#### 搜索文件
```
你: 搜索所有 .py 文件
Suna: ✓ 搜索完成，找到 3 个匹配项
    - src/main.py
    - src/agent/agent.py
    - run.py
```

#### 复制和移动文件
```
你: 将 notes.txt 复制到 backup/ 目录
Suna: ✓ 复制文件成功: notes.txt -> backup/notes.txt
```

#### 批量操作
```
你: 创建三个Python文件：main.py, utils.py, config.py，每个文件都包含基本的Python代码结构
Suna: [依次创建三个文件，每个都包含完整的Python代码结构]
```

## 命令行操作

### 基本命令执行

#### 系统信息查询
```
你: 查看当前系统的信息
Suna: ✓ 命令执行成功
    系统: Windows 10
    架构: AMD64
    Python版本: 3.11.0
    当前目录: C:\Users\user\suna-lite
```

#### 目录操作
```
你: 在当前目录创建一个名为 test_project 的新目录
Suna: ✓ 创建目录成功: test_project
```

### 编程相关命令

#### Python 包管理
```
你: 安装 requests 包
Suna: ✓ 命令执行成功
    Collecting requests
    Downloading requests-2.31.0-py3-none-any.whl (62 kB)
    Successfully installed requests-2.31.0
```

#### 代码执行
```
你: 运行一个简单的Python脚本，打印 "Hello, World!"
Suna: ✓ 命令执行成功
    Hello, World!
```

### 网络命令

#### 网络测试
```
你: 测试网络连接，ping google.com
Suna: ✓ 命令执行成功
    PING google.com (142.250.191.78) 56(84) bytes of data.
    Reply from 142.250.191.78: bytes=56 time=15ms TTL=118
```

#### 文件下载
```
你: 下载一个示例文件
Suna: ✓ 命令执行成功
    --2024-01-01 12:00:00--  https://example.com/sample.txt
    Resolving example.com... 93.184.216.34
    Connecting to example.com|93.184.216.34|:443... connected.
    HTTP request sent, awaiting response... 200 OK
```

## Web 搜索

### 基本搜索

#### 信息搜索
```
你: 搜索 "Python 3.11 的新特性"
Suna: ✓ 搜索完成，找到 8 个结果
    1. Python 3.11 正式发布：有哪些新特性？
    2. Python 3.11 新特性详解：更好的错误消息...
    3. Python 3.11 性能提升和新功能介绍...
```

#### 新闻搜索
```
你: 搜索最新的 AI 发展新闻
Suna: ✓ 搜索完成，找到 10 个结果
    [显示最新的AI新闻和趋势]
```

### 内容获取

#### 网页内容提取
```
你: 获取维基百科上 "人工智能" 页面的主要内容
Suna: ✓ 成功获取网页内容: 人工智能 - 维基百科
    人工智能（AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的机器...
```

#### 结构化数据提取
```
你: 提取当前网页的所有链接
Suna: ✓ 成功提取 links 内容
    - 首页: https://example.com/
    - 关于我们: https://example.com/about
    - 产品: https://example.com/products
```

### 页面分析

#### 页面结构分析
```
你: 分析 https://example.com 的页面结构
Suna: ✓ 页面分析完成: Example Domain
    标题: Example Domain
    标题层级: h1: 1, h2: 2, h3: 3
    链接数量: 15
    图片数量: 3
    关键词: example, domain, page
```

## 浏览器自动化

### 基本网页操作

#### 网页导航
```
你: 打开百度首页
Suna: ✓ 成功导航到: https://www.baidu.com
```

#### 搜索操作
```
你: 在百度搜索 "Suna-Lite AI 助手"
Suna: ✓ 成功点击元素: #kw
    ✓ 成功填写表单: #kw = Suna-Lite AI 助手
    ✓ 成功提交表单
```

### 表单交互

#### 登录表单
```
你: 填写登录表单，用户名为 test@example.com，密码为 password123
Suna: ✓ 成功填写表单: #username = test@example.com
    ✓ 成功填写表单: #password = password123
    ✓ 成功提交表单
```

#### 复杂表单
```
你: 填写注册表单，包括用户名、邮箱、密码等信息
Suna: [自动识别表单字段并依次填写]
```

### 数据提取

#### 表格数据提取
```
你: 提取当前页面中的所有表格数据
Suna: ✓ 成功提取 tables 内容
    表格 1 (3行 x 4列):
    | 姓名 | 年龄 | 职业 | 城市 |
    |-----|-----|-----|-----|
    | 张三 | 25  | 工程师 | 北京 |
    | 李四 | 30  | 设计师 | 上海 |
```

#### 列表数据提取
```
你: 提取页面中的所有产品列表
Suna: ✓ 成功提取内容
    产品列表：
    1. 产品A - 价格: ¥100
    2. 产品B - 价格: ¥200
    3. 产品C - 价格: ¥300
```

## 会话管理

### 查看会话状态

#### 工作区信息
```
你: /workspace
Suna: 
    工作区路径: ./workspace/session_123456
    文件数量: 15
    目录数量: 8
    总大小: 2.3 MB
```

#### 配置信息
```
你: /config
Suna: 
    **AI配置**
    - 模型: Qwen/Qwen3-Coder-480B-A35B-Instruct
    - 最大令牌: 4000
    - 温度: 0.7
    
    **工具状态**
    - 文件操作: ✓
    - 命令执行: ✓
    - Web搜索: ✓
    - 浏览器自动化: ✓
```

### 历史管理

#### 清空历史
```
你: /clear
Suna: ✓ 对话历史已清空
```

#### 重置状态
```
你: /reset
Suna: ✓ Agent状态已重置
```

## 实用技巧

### 1. 任务分解
将复杂任务分解为多个小步骤：

```
❌ 不好的方式：
你: 创建一个完整的网站

✅ 好的方式：
你: 我需要创建一个网站，请按以下步骤进行：
    1. 创建项目目录结构
    2. 创建 HTML 文件
    3. 添加 CSS 样式
    4. 添加 JavaScript 功能
```

### 2. 具体指令
提供具体明确的指令：

```
❌ 不好的方式：
你: 处理一下这个文件

✅ 好的方式：
你: 读取 data.txt 文件，统计每个单词出现的频率，然后将结果保存到 word_count.txt 中
```

### 3. 错误处理
当遇到错误时，询问具体原因：

```
你: 之前的操作失败了，请告诉我具体的错误信息，我会尝试其他方法
```

### 4. 批量操作
利用工具的批量处理能力：

```
你: 将当前目录下所有的 .txt 文件转换成 .md 文件，保持文件名不变
```

### 5. 数据处理
组合多个工具进行数据处理：

```
你: 下载这个 CSV 文件，用 Python 分析数据，生成图表，并将结果保存为 PDF
```

## 高级功能

### 自定义配置
您可以通过修改 `config.yaml` 来自定义：
- AI 模型参数
- 工具开关
- 工作区设置
- 安全策略

### 脚本自动化
创建脚本文件来自动化重复任务：

```
你: 创建一个名为 backup.py 的脚本，用于自动备份工作区中的重要文件
```

### 批量处理
利用 AI 的理解能力进行批量操作：

```
你: 分析当前目录中的所有 Python 文件，找出其中可能存在安全问题的代码模式
```

## 注意事项

### 安全提醒
- 不要执行来自不可信来源的命令
- 谨慎处理敏感文件和数据
- 定期清理工作区中的临时文件
- 注意保护 API 密钥和私人信息

### 性能优化
- 定期清理对话历史以提高响应速度
- 使用 `/clear` 命令清空不需要的历史记录
- 关闭不需要的工具功能以减少资源占用

### 最佳实践
- 使用具体明确的指令
- 将复杂任务分解为简单步骤
- 定期备份重要的工作文件
- 保持工作区整洁有序

---

## 更多资源

- [架构文档](ARCHITECTURE.md) - 深入了解系统设计
- [使用示例](EXAMPLES.md) - 更多实际应用案例
- [故障排除](INSTALLATION.md#故障排除) - 常见问题解决
- [GitHub Issues](https://github.com/IhyaH/suna-lite/issues) - 问题反馈和讨论

希望这份使用说明能帮助您更好地使用 Suna-Lite！如有任何问题，请随时联系我们。