#!/usr/bin/env python3
"""
Suna-Lite 配置逻辑演示脚本

展示当前配置系统的加载逻辑和优先级
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def analyze_config_logic():
    """分析配置逻辑"""
    print("=" * 60)
    print("Suna-Lite 配置逻辑分析")
    print("=" * 60)
    
    print("\n当前配置加载逻辑:")
    print("1. 检查环境变量中的必需配置 (OPENAI_API_KEY, OPENAI_BASE_URL)")
    print("2. 如果环境变量存在且有效 -> 优先使用环境变量")
    print("3. 如果环境变量缺失 -> 使用YAML配置文件")
    print("4. 如果YAML文件也不存在 -> 使用默认配置")
    
    print("\n详细流程分析:")
    
    # 测试当前配置状态
    from src.config.env_loader import load_env, validate_required_env_vars
    from src.config.settings import Settings
    
    print("\n第一步: 加载环境变量")
    env_vars = load_env()
    print(f"环境变量中的API_KEY: {'已设置' if env_vars.get('OPENAI_API_KEY') else '未设置'}")
    print(f"环境变量中的BASE_URL: {'已设置' if env_vars.get('OPENAI_BASE_URL') else '未设置'}")
    print(f"环境变量中的MODEL: {env_vars.get('OPENAI_MODEL', '未设置')}")
    
    print("\n第二步: 验证必需环境变量")
    has_required = validate_required_env_vars()
    print(f"必需环境变量验证结果: {'通过' if has_required else '失败'}")
    
    print("\n第三步: 实际配置加载")
    settings = Settings.load_with_priority('config.yaml')
    print(f"实际使用的配置来源: {'环境变量' if has_required else 'YAML文件'}")
    print(f"模型: {settings.agent.model}")
    print(f"Base URL: {settings.agent.base_url}")
    print(f"工作区路径: {settings.workspace.path}")
    print(f"日志级别: {settings.logging.level}")
    
    return settings, has_required

def show_config_priority():
    """展示配置优先级规则"""
    print("\n" + "=" * 60)
    print("配置优先级规则")
    print("=" * 60)
    
    print("\n优先级从高到低:")
    print("1. 环境变量 (.env文件) - 最高优先级")
    print("2. YAML配置文件 (config.yaml) - 中等优先级")
    print("3. 默认值 - 最低优先级")
    
    print("\n具体规则:")
    print("- AI配置 (model, base_url, api_key): 环境变量优先，YAML只作补充")
    print("- 其他配置 (workspace, browser, tools等): YAML可以覆盖环境变量")
    print("- 必需配置缺失时: 系统会报错")
    
    print("\n使用建议:")
    print("- 开发环境: 使用YAML文件配置，.env文件留空或注释")
    print("- 生产环境: 使用环境变量覆盖敏感信息")
    print("- 测试环境: 可以创建不同的YAML配置文件")

def main():
    """主函数"""
    print("开始分析Suna-Lite配置逻辑...")
    
    # 分析配置逻辑
    settings, has_required = analyze_config_logic()
    
    # 显示优先级规则
    show_config_priority()
    
    print("\n" + "=" * 60)
    print("配置逻辑分析完成")
    print("=" * 60)
    
    print(f"\n总结:")
    print(f"- 当前配置来源: {'环境变量' if has_required else 'YAML文件'}")
    print(f"- 模型: {settings.agent.model}")
    print(f"- Base URL: {settings.agent.base_url}")
    print(f"- 配置验证: {'通过' if settings.validate() else '失败'}")

if __name__ == "__main__":
    main()