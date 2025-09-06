# Suna-Lite 使用示例

本文档提供 Suna-Lite 的实际使用示例，展示各种功能的应用场景和最佳实践。

## 基础使用示例

### 1. 文件操作示例

#### 创建和编辑文件

```
你: 创建一个名为 hello.py 的文件，内容为打印 "Hello, Suna-Lite!"
Suna: ✓ 创建文件成功: hello.py

你: 读取 hello.py 文件的内容
Suna: ✓ 读取文件成功: hello.py
    print("Hello, Suna-Lite!")

你: 在 hello.py 文件中添加一个函数，计算两个数的和
Suna: ✓ 写入文件成功: hello.py
    def add_numbers(a, b):
        return a + b
    
    print("Hello, Suna-Lite!")
    result = add_numbers(5, 3)
    print(f"5 + 3 = {result}")
```

#### 批量文件操作

```
你: 创建三个文件：config.py、utils.py、main.py，每个文件都包含基本的Python代码结构
Suna: ✓ 创建文件成功: config.py
    # 配置文件
    DATABASE_URL = "sqlite:///app.db"
    DEBUG = True
    
    ✓ 创建文件成功: utils.py
    # 工具函数
    def format_date(date):
        return date.strftime("%Y-%m-%d")
    
    def calculate_total(items):
        return sum(item['price'] for item in items)
    
    ✓ 创建文件成功: main.py
    # 主程序
    from config import DATABASE_URL, DEBUG
    from utils import format_date, calculate_total
    
    def main():
        print("应用程序启动")
        print(f"调试模式: {DEBUG}")
        print(f"数据库: {DATABASE_URL}")
    
    if __name__ == "__main__":
        main()
```

### 2. 目录管理示例

#### 创建项目结构

```
你: 创建一个完整的项目结构，包括 src/、tests/、docs/ 目录和相应的文件
Suna: ✓ 创建目录成功: src/
    ✓ 创建目录成功: tests/
    ✓ 创建目录成功: docs/
    ✓ 创建文件成功: src/__init__.py
    ✓ 创建文件成功: tests/test_main.py
    ✓ 创建文件成功: docs/README.md

你: 列出当前目录的完整结构
Suna: ✓ 列出目录成功: . (8 项)
    目录: src/
    目录: tests/
    目录: docs/
    文件: config.py
    文件: utils.py
    文件: main.py
    文件: hello.py
    文件: requirements.txt
```

## 命令行操作示例

### 1. 系统信息查询

```
你: 查看当前系统的详细信息，包括Python版本、操作系统和当前目录
Suna: ✓ 命令执行成功
    系统: Windows 10
    架构: AMD64
    Python版本: 3.11.0
    当前目录: C:\Users\user\suna-lite
    工作区: ./workspace/session_123456
```

### 2. 开发环境操作

#### Python 包管理

```
你: 安装 requests 和 beautifulsoup4 包
Suna: ✓ 命令执行成功
    Collecting requests
      Downloading requests-2.31.0-py3-none-any.whl (62 kB)
    Collecting beautifulsoup4
      Downloading beautifulsoup4-4.12.2-py3-none-any.whl (142 kB)
    Successfully installed requests-2.31.0 beautifulsoup4-4.12.2

你: 创建 requirements.txt 文件，列出当前安装的所有包
Suna: ✓ 命令执行成功
    ✓ 创建文件成功: requirements.txt
    openai==1.3.0
    requests==2.31.0
    beautifulsoup4==4.12.2
    click==8.1.7
    rich==13.6.0
```

#### 代码执行和测试

```
你: 运行 hello.py 文件
Suna: ✓ 命令执行成功
    Hello, Suna-Lite!
    5 + 3 = 8

你: 检查当前目录中所有Python文件的语法错误
Suna: ✓ 命令执行成功
    ✓ config.py 语法正确
    ✓ utils.py 语法正确
    ✓ main.py 语法正确
    ✓ hello.py 语法正确
```

### 3. 文件系统操作

#### 文件搜索和统计

```
你: 搜索所有包含 "import" 关键字的Python文件
Suna: ✓ 搜索完成，找到 3 个匹配项
    - main.py: 包含 2 个 import 语句
    - utils.py: 包含 1 个 import 语句
    - hello.py: 包含 0 个 import 语句

你: 统计当前目录中各种文件类型的数量
Suna: ✓ 命令执行成功
    文件类型统计:
    - .py: 4 个文件
    - .txt: 1 个文件
    - .md: 3 个文件
    - .yaml: 1 个文件
```

## Web 搜索示例

### 1. 信息搜索

#### 技术文档搜索

```
你: 搜索 "Python 3.11 新特性" 并总结主要内容
Suna: ✓ 搜索完成，找到 8 个结果
    1. Python 3.11 正式发布：有哪些新特性？
    2. Python 3.11 新特性详解：更好的错误消息...
    3. Python 3.11 性能提升和新功能介绍...
    
    主要新特性：
    - 更好的错误消息和异常处理
    - 性能提升（比3.10快10-60%）
    - 新的 typing 功能
    - 异步迭代器改进
    - 异常组功能
```

#### 新闻和趋势搜索

```
你: 搜索最新的 AI 发展趋势
Suna: ✓ 搜索完成，找到 10 个结果
    1. 2024年AI发展趋势：多模态AI的崛起
    2. GPT-4在各个领域的应用案例
    3. AI在软件开发中的最新应用...
    
    AI发展趋势：
    - 多模态AI模型（文本、图像、音频）
    - AI辅助编程工具的普及
    - 大型语言模型的小型化
    - AI在边缘计算中的应用
```

### 2. 内容获取和分析

#### 网页内容提取

```
你: 获取维基百科上 "人工智能" 页面的主要内容
Suna: ✓ 成功获取网页内容: 人工智能 - 维基百科
    人工智能（AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的机器...
    
    主要内容包括：
    - AI的定义和历史发展
    - 主要技术和方法
    - 应用领域和案例
    - 伦理和社会影响
```

#### 结构化数据提取

```
你: 分析 https://example.com/products 页面，提取所有产品信息
Suna: ✓ 页面分析完成: Example Products
    提取到 5 个产品：
    1. 产品A - 价格: $99.99 - 描述: 高性能处理器
    2. 产品B - 价格: $149.99 - 描述: 大容量存储设备
    3. 产品C - 价格: $79.99 - 描述: 无线网络适配器
    4. 产品D - 价格: $199.99 - 描述: 专业显卡
    5. 产品E - 价格: $29.99 - 描述: 机械键盘
```

## 浏览器自动化示例

### 1. 网页交互

#### 搜索引擎操作

```
你: 打开百度，搜索 "Suna-Lite AI 助手"
Suna: ✓ 成功导航到: https://www.baidu.com
    ✓ 成功填写搜索框: Suna-Lite AI 助手
    ✓ 成功提交搜索
    ✓ 搜索结果页面已加载
    
    搜索结果摘要：
    - 找到约 1,000,000 个相关结果
    - 前5个结果包含相关技术文章
    - 搜索用时 0.32 秒
```

#### 表单填写和提交

```
你: 填写一个注册表单，包含用户名、邮箱、密码等信息
Suna: ✓ 成功填写表单字段：
    - 用户名: testuser2024
    - 邮箱: testuser@example.com
    - 密码: [已隐藏]
    - 确认密码: [已隐藏]
    ✓ 成功提交表单
    ✓ 注册成功页面已加载
```

### 2. 数据抓取

#### 表格数据提取

```
你: 提取当前页面中的所有表格数据
Suna: ✓ 成功提取 tables 内容
    表格 1 (5行 x 4列):
    | 姓名 | 年龄 | 职业 | 城市 |
    |-----|-----|-----|-----|
    | 张三 | 25  | 工程师 | 北京 |
    | 李四 | 30  | 设计师 | 上海 |
    | 王五 | 28  | 产品经理 | 深圳 |
    | 赵六 | 35  | 数据分析师 | 杭州 |
```

#### 列表数据提取

```
你: 提取页面中的所有文章列表，包括标题、作者和发布时间
Suna: ✓ 成功提取文章列表
    文章列表（共10篇）：
    1. 标题: "Python异步编程完全指南" 
       作者: 张三 
       发布时间: 2024-01-15
    
    2. 标题: "Docker容器化部署实践" 
       作者: 李四 
       发布时间: 2024-01-14
    
    3. 标题: "机器学习在金融领域的应用" 
       作者: 王五 
       发布时间: 2024-01-13
```

## 数据处理和分析示例

### 1. 数据分析

```
你: 分析当前工作区的文件类型分布，并生成统计报告
Suna: ✓ 成功生成文件类型统计报告
    
    工作区文件分析报告
    ====================
    
    总文件数: 23
    总目录数: 8
    总大小: 1.2 MB
    
    文件类型分布:
    - Python文件 (.py): 12 个 (52.2%)
    - 文本文件 (.txt): 5 个 (21.7%)
    - 文档文件 (.md): 4 个 (17.4%)
    - 配置文件 (.yaml/.yml): 2 个 (8.7%)
    
    最大文件: src/agent/agent.py (45.2 KB)
    最新文件: docs/EXAMPLES.md (刚刚创建)
```

### 2. 日志分析

```
你: 分析 suna-lite.log 文件，提取错误信息和统计
Suna: ✓ 成功分析日志文件
    
    日志分析报告
    =============
    
    分析时间范围: 2024-01-01 10:00:00 - 2024-01-01 18:00:00
    
    日志级别统计:
    - INFO: 1,234 条 (85.2%)
    - WARNING: 156 条 (10.8%)
    - ERROR: 45 条 (3.1%)
    - DEBUG: 12 条 (0.9%)
    
    错误信息摘要:
    1. FileNotFoundError: 文件不存在 (15 次)
    2. ConnectionError: 网络连接失败 (12 次)
    3. TimeoutError: 操作超时 (8 次)
    4. PermissionError: 权限不足 (6 次)
    5. ValueError: 参数错误 (4 次)
```

## 开发工作流示例

### 1. 项目初始化

```
你: 创建一个新的Python项目，包含完整的项目结构
Suna: ✓ 创建项目成功: my_new_project/
    
    项目结构:
    my_new_project/
    ├── src/
    │   ├── __init__.py
    │   ├── main.py
    │   └── utils.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_main.py
    │   └── test_utils.py
    ├── docs/
    │   └── README.md
    ├── requirements.txt
    ├── setup.py
    └── README.md
    
    ✓ 创建文件成功: src/main.py
    ✓ 创建文件成功: src/utils.py
    ✓ 创建文件成功: tests/test_main.py
    ✓ 创建文件成功: requirements.txt
    ✓ 创建文件成功: setup.py
    ✓ 创建文件成功: README.md
```

### 2. 代码质量检查

```
你: 对项目进行代码质量检查，包括语法检查、格式检查和类型检查
Suna: ✓ 开始代码质量检查
    
    1. 语法检查 (flake8):
       ✓ src/main.py - 无语法错误
       ✓ src/utils.py - 无语法错误
       ✓ tests/test_main.py - 无语法错误
    
    2. 代码格式化 (black):
       ✓ 代码格式检查通过
       ✓ 自动格式化 3 个文件
    
    3. 类型检查 (mypy):
       ✓ 类型检查通过
       ✓ 发现 0 个类型错误
    
    代码质量检查完成 - 所有检查均通过！
```

### 3. 测试执行

```
你: 运行项目的所有测试，并生成覆盖率报告
Suna: ✓ 开始运行测试
    
    pytest 输出:
    ============================= test session starts ==============================
    collected 8 items
    
    tests/test_main.py ...                                                 [ 37%]
    tests/test_utils.py .....                                             [ 87%]
    tests/test_integration.py .                                          [100%]
    
    ============================== 8 passed in 0.45s ===============================
    
    测试覆盖率:
    - src/main.py: 95%
    - src/utils.py: 88%
    - 总体覆盖率: 92%
    
    所有测试通过！覆盖率达标。
```

## 高级功能示例

### 1. 自动化脚本创建

```
你: 创建一个自动化脚本，用于备份工作区中的重要文件
Suna: ✓ 创建文件成功: backup_script.py
    
    #!/usr/bin/env python3
    """
    工作区备份脚本
    自动备份工作区中的重要文件到指定目录
    """
    
    import os
    import shutil
    from datetime import datetime
    import zipfile
    
    def backup_workspace(source_dir, backup_dir, file_extensions=None):
        """备份工作区文件"""
        
        if file_extensions is None:
            file_extensions = ['.py', '.md', '.txt', '.yaml', '.yml']
        
        # 创建备份目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
        os.makedirs(backup_path, exist_ok=True)
        
        # 复制文件
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_path, source_dir)
                    dst_path = os.path.join(backup_path, rel_path)
                    
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.copy2(src_path, dst_path)
        
        # 创建压缩包
        zip_path = f"{backup_path}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_path)
                    zipf.write(file_path, arcname)
        
        # 删除临时目录
        shutil.rmtree(backup_path)
        
        return zip_path
    
    if __name__ == "__main__":
        source = "./workspace"
        backup_dir = "./backups"
        result = backup_workspace(source, backup_dir)
        print(f"备份完成: {result}")
```

### 2. 网络监控脚本

```
你: 创建一个网络监控脚本，检查网站可用性和响应时间
Suna: ✓ 创建文件成功: network_monitor.py
    
    #!/usr/bin/env python3
    """
    网络监控脚本
    监控指定网站的可用性和响应时间
    """
    
    import requests
    import time
    from datetime import datetime
    import json
    
    def check_website(url, timeout=10):
        """检查网站状态"""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=timeout)
            response_time = (time.time() - start_time) * 1000
            
            return {
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'available': response.status_code == 200,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'available': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def monitor_websites(urls, interval=60):
        """监控多个网站"""
        results = []
        
        for url in urls:
            result = check_website(url)
            results.append(result)
            print(f"检查 {url}: {'✓' if result['available'] else '✗'}")
            
            if interval > 0:
                time.sleep(interval)
        
        return results
    
    if __name__ == "__main__":
        websites = [
            "https://www.google.com",
            "https://www.github.com",
            "https://www.python.org"
        ]
        
        print("开始网络监控...")
        results = monitor_websites(websites)
        
        # 保存结果
        with open("monitor_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"监控完成，结果已保存到 monitor_results.json")
```

### 3. 数据处理管道

```
你: 创建一个数据处理脚本，读取CSV文件，分析数据并生成报告
Suna: ✓ 创建文件成功: data_processor.py
    
    #!/usr/bin/env python3
    """
    数据处理脚本
    读取CSV文件，分析数据并生成报告
    """
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from datetime import datetime
    
    def analyze_data(file_path):
        """分析数据文件"""
        
        # 读取数据
        df = pd.read_csv(file_path)
        
        # 基本统计
        stats = {
            'total_records': len(df),
            'columns': list(df.columns),
            'data_types': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'numeric_stats': df.describe().to_dict()
        }
        
        # 生成可视化
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) > 0:
            plt.figure(figsize=(12, 8))
            
            # 创建子图
            for i, col in enumerate(numeric_columns[:4], 1):
                plt.subplot(2, 2, i)
                df[col].hist(bins=20)
                plt.title(f'{col} 分布')
                plt.xlabel(col)
                plt.ylabel('频次')
            
            plt.tight_layout()
            plt.savefig('data_analysis.png')
            plt.close()
        
        # 生成报告
        report = generate_report(df, stats)
        
        return stats, report
    
    def generate_report(df, stats):
        """生成分析报告"""
        
        report = f"""
        数据分析报告
        ============
        
        生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        数据概览:
        - 总记录数: {stats['total_records']}
        - 列数: {len(stats['columns'])}
        - 列名: {', '.join(stats['columns'])}
        
        数据类型:
        """
        
        for col, dtype in stats['data_types'].items():
            report += f"- {col}: {dtype}\n"
        
        report += "\n缺失值统计:\n"
        for col, missing in stats['missing_values'].items():
            if missing > 0:
                report += f"- {col}: {missing} 个缺失值\n"
        
        return report
    
    if __name__ == "__main__":
        input_file = "data.csv"
        
        print(f"开始分析数据文件: {input_file}")
        stats, report = analyze_data(input_file)
        
        # 保存报告
        with open("analysis_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        
        print("分析完成！")
        print(f"- 统计信息已保存")
        print(f"- 可视化图表已保存为 data_analysis.png")
        print(f"- 分析报告已保存为 analysis_report.txt")
```

## 批量操作示例

### 1. 批量文件转换

```
你: 将当前目录下所有的 .txt 文件转换为 .md 文件，保持文件名不变
Suna: ✓ 开始批量文件转换
    
    处理进度:
    ✓ notes.txt → notes.md
    ✓ readme.txt → readme.md
    ✓ changelog.txt → changelog.md
    
    转换完成！共转换 3 个文件。
    
    转换详情:
    - notes.txt (1.2 KB) → notes.md (1.3 KB)
    - readme.txt (3.5 KB) → readme.md (3.8 KB)  
    - changelog.txt (2.1 KB) → changelog.md (2.4 KB)
```

### 2. 批量代码分析

```
你: 分析当前目录中所有Python文件的复杂度和代码质量
Suna: ✓ 开始代码质量分析
    
    分析结果:
    =========
    
    文件: src/main.py
    - 代码行数: 156
    - 函数数量: 8
    - 类数量: 2
    - 平均圈复杂度: 3.2
    - 代码质量: 优秀
    
    文件: src/utils.py
    - 代码行数: 89
    - 函数数量: 5
    - 类数量: 1
    - 平均圈复杂度: 2.1
    - 代码质量: 优秀
    
    文件: src/agent/agent.py
    - 代码行数: 234
    - 函数数量: 12
    - 类数量: 3
    - 平均圈复杂度: 4.5
    - 代码质量: 良好
    
    总体统计:
    - 总文件数: 3
    - 总代码行数: 479
    - 总函数数: 25
    - 总类数: 6
    - 平均复杂度: 3.3
    - 总体质量: 良好
```

## 自定义配置示例

### 1. 自定义AI模型配置

```
你: 修改配置文件，使用不同的AI模型和参数
Suna: ✓ 配置文件已更新
    
    配置更改:
    - 模型: gpt-3.5-turbo → gpt-4
    - 温度: 0.7 → 0.3
    - 最大令牌: 4000 → 8000
    - 对话历史: 10 → 20
    
    新配置已生效，下次对话将使用新的AI模型设置。
```

### 2. 工具开关配置

```
你: 禁用浏览器自动化功能，启用文件操作和Web搜索
Suna: ✓ 工具配置已更新
    
    工具状态:
    - 文件操作: ✓ 启用
    - Shell命令: ✓ 启用
    - Web搜索: ✓ 启用
    - 浏览器自动化: ✗ 禁用
    
    配置已生效，浏览器自动化工具将不再可用。
```

## 学习和教程示例

### 1. Python学习助手

```
你: 创建一个Python学习教程，包含基础语法和示例代码
Suna: ✓ 创建Python学习教程: python_tutorial.md
    
    # Python 基础教程
    
    ## 1. 变量和数据类型
    
    ```python
    # 变量赋值
    name = "Python"
    version = 3.11
    is_popular = True
    
    # 数据类型
    text = "Hello, World!"  # 字符串
    number = 42            # 整数
    decimal = 3.14         # 浮点数
    active = True          # 布尔值
    items = [1, 2, 3]      # 列表
    person = {"name": "Alice", "age": 25}  # 字典
    ```
    
    ## 2. 控制结构
    
    ```python
    # 条件语句
    if age >= 18:
        print("成年人")
    elif age >= 13:
        print("青少年")
    else:
        print("儿童")
    
    # 循环
    for i in range(5):
        print(f"数字: {i}")
    
    while count > 0:
        print(f"倒计时: {count}")
        count -= 1
    ```
    
    [继续输出完整的教程内容...]
```

### 2. 项目实战案例

```
你: 创建一个简单的Web爬虫项目，包含完整的项目结构和文档
Suna: ✓ 创建Web爬虫项目: web_scraper/
    
    项目结构:
    web_scraper/
    ├── src/
    │   ├── __init__.py
    │   ├── scraper.py
    │   ├── parser.py
    │   └── storage.py
    ├── tests/
    │   ├── test_scraper.py
    │   └── test_parser.py
    ├── data/
    │   └── output/
    ├── config/
    │   └── settings.py
    ├── requirements.txt
    ├── README.md
    └── main.py
    
    [创建各文件内容...]
```

## 故障排除示例

### 1. 网络连接问题

```
你: 诊断网络连接问题，测试OpenAI API的连通性
Suna: ✓ 开始网络诊断
    
    诊断结果:
    =========
    
    1. 基础网络连接:
       ✓ DNS解析正常
       ✓ 网络连接正常
    
    2. OpenAI API测试:
       - API端点: https://openai.ihyah.top/
       - 响应时间: 1.2秒
       - 状态码: 200
       ✓ API连接正常
    
    3. 本地配置检查:
       ✓ API密钥已配置
       ✓ Agent设置正常
       ✓ 防火墙允许连接
    
    建议: 网络连接正常，如果仍有问题请检查API密钥有效性。
```

### 2. 权限问题解决

```
你: 检查并修复文件权限问题
Suna: ✓ 开始权限检查
    
    权限检查结果:
    ==============
    
    1. 工作区权限:
       ✓ 读取权限: 正常
       ✓ 写入权限: 正常
       ✓ 执行权限: 正常
    
    2. 配置文件权限:
       ✓ config.yaml: 可读写
       ✓ .env: 可读写
    
    3. Python环境权限:
       ✓ 包安装权限: 正常
       ✓ 脚本执行权限: 正常
    
    权限状态: 所有权限正常，无需修复。
```

---

这些示例展示了 Suna-Lite 的各种使用场景和功能。通过这些实际案例，您可以更好地理解如何使用 Suna-Lite 来完成各种任务，从简单的文件操作到复杂的自动化流程。