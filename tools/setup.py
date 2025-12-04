#!/usr/bin/env python3
"""
项目设置脚本
"""
import os
import subprocess
import sys

def run_command(cmd, description):
    """运行命令并处理错误"""
    print(f"正在执行: {description}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✓ {description} 完成")
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} 失败: {e}")
        sys.exit(1)

def main():
    print("=== 项目设置脚本 ===")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 创建虚拟环境
    if not os.path.exists("venv"):
        run_command("python -m venv venv", "创建虚拟环境")
    
    # 安装依赖
    run_command("venv\\Scripts\\pip install -r requirements\\dev.txt", "安装开发依赖")
    
    # 运行数据库迁移
    run_command("venv\\Scripts\\python manage.py migrate", "运行数据库迁移")
    
    # 创建超级用户
    print("\n=== 创建超级用户 ===")
    run_command("venv\\Scripts\\python manage.py createsuperuser", "创建超级用户")
    
    print("\n=== 设置完成 ===")
    print("请激活虚拟环境: venv\\Scripts\\activate")
    print("然后运行: python manage.py runserver")

if __name__ == "__main__":
    main()