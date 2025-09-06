#!/usr/bin/env python3
"""
Suna-Lite 配置逻辑演示脚本

展示当前配置系统的加载逻辑和优先级
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def demonstrate_config_logic():
    """演示配置逻辑"""
    print("=" * 60)
    print("Suna-Lite 配置逻辑演示")
    print("=" * 60)
    
    print("\n[配置] 当前配置加载逻辑:")
    print("1. 检查YAML配置文件 (config.yaml)")
    print("2. 如果YAML文件存在且有效 -> 使用YAML配置")
    print("3. 如果YAML文件不存在 -> 使用默认配置")
    print("4. 环境变量不再用于配置（简化后的设计）")
    
    print("\n[分析] 详细流程分析:")
    
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
    
    return settings

def show_config_priority():
    """展示配置优先级规则"""
    print("\n" + "=" * 60)
    print("配置优先级规则")
    print("=" * 60)
    
    print("\n[优先级] 配置优先级规则:")
    print("1. YAML配置文件 (config.yaml) - 唯一配置源")
    print("2. 默认值 - 备用配置")
    
    print("\n[规则] 具体规则:")
    print("- 所有配置都从YAML文件加载")
    print("- 如果YAML文件不存在，使用默认配置")
    print("- 环境变量不再用于配置（为了简化）")
    
    print("\n[建议] 使用建议:")
    print("- 所有配置都在config.yaml文件中管理")
    print("- 敏感信息请妥善保管config.yaml文件")
    print("- 可以创建不同的YAML配置文件用于不同环境")

def show_current_config():
    """显示当前配置状态"""
    print("\n" + "=" * 60)
    print("当前配置状态")
    print("=" * 60)
    
    try:
        from src.config.settings import Settings
        
        settings = Settings.load_with_priority('config.yaml')
        
        print("\n[AI] AI代理配置:")
        print(f"  模型: {settings.agent.model}")
        print(f"  Base URL: {settings.agent.base_url}")
        print(f"  API Key: {settings.agent.api_key[:20]}...")
        print(f"  最大令牌: {settings.agent.max_tokens}")
        print(f"  温度: {settings.agent.temperature}")
        
        print("\n[工作区] 工作区配置:")
        print(f"  路径: {settings.workspace.path}")
        print(f"  最大大小: {settings.workspace.max_size_mb}MB")
        print(f"  自动清理: {settings.workspace.auto_cleanup}")
        
        print("\n[浏览器] 浏览器配置:")
        print(f"  无头模式: {settings.browser.headless}")
        print(f"  超时时间: {settings.browser.timeout_seconds}秒")
        
        print("\n[工具] 工具配置:")
        print(f"  文件操作: {settings.tools.file_operations}")
        print(f"  Shell命令: {settings.tools.shell_commands}")
        print(f"  Web搜索: {settings.tools.web_search}")
        print(f"  浏览器自动化: {settings.tools.browser_automation}")
        
        print("\n[日志] 日志配置:")
        print(f"  级别: {settings.logging.level}")
        print(f"  文件: {settings.logging.file}")
        print(f"  最大大小: {settings.logging.max_size_mb}MB")
        
        print(f"\n[验证] 配置验证结果: {'通过' if settings.validate() else '失败'}")
        
    except Exception as e:
        print(f"[错误] 配置加载失败: {e}")

def main():
    """主函数"""
    print("开始分析Suna-Lite配置逻辑...")
    
    # 演示配置逻辑
    settings = demonstrate_config_logic()
    
    # 显示优先级规则
    show_config_priority()
    
    # 显示当前配置
    show_current_config()
    
    print("\n" + "=" * 60)
    print("配置逻辑分析完成")
    print("=" * 60)

if __name__ == "__main__":
    main()