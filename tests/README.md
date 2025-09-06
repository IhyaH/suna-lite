# Tests and Scripts Directory

## Directory Structure

```
tests/           # 测试脚本目录
├── test_functionality.py    # 功能测试
├── test_tools.py           # 工具测试
├── test_conversation.py    # 对话测试
└── test_all_tools.py       # 所有工具测试

scripts/         # 实用脚本目录
├── config_analysis.py      # 配置分析脚本
└── analyze_config.py       # 配置分析脚本（备用）
```

## Usage

### Running Tests

```bash
# 运行功能测试
python tests/test_functionality.py

# 运行工具测试
python tests/test_tools.py

# 运行对话测试
python tests/test_conversation.py

# 运行所有工具测试
python tests/test_all_tools.py
```

### Running Scripts

```bash
# 分析配置文件
python scripts/config_analysis.py

# 分析配置（备用方法）
python scripts/analyze_config.py
```

## Adding New Tests

1. 创建新的测试文件时，请使用 `test_` 前缀
2. 将测试文件放置在 `tests/` 目录中
3. 实用脚本放置在 `scripts/` 目录中
4. 确保测试文件有适当的文档字符串