#!/usr/bin/env python3
"""
脚本用于检测setup.py中的版本号变化
"""
import re
import subprocess
import sys
from pathlib import Path


def get_version_from_setup(setup_path):
    """从setup.py文件中提取版本号"""
    with open(setup_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式匹配版本号
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return None


def get_previous_setup_content():
    """获取上一个提交中的setup.py内容"""
    try:
        result = subprocess.run(['git', 'show', 'HEAD~1:setup.py'], 
                              capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        # 如果是第一个提交，则没有上一个版本
        return None


def get_previous_version():
    """获取上一个提交中的版本号"""
    content = get_previous_setup_content()
    if content:
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    return None


def main():
    current_setup_path = Path('setup.py')
    if not current_setup_path.exists():
        print("Error: setup.py not found")
        sys.exit(1)

    current_version = get_version_from_setup(current_setup_path)
    previous_version = get_previous_version()

    print(f"Current version: {current_version}")
    print(f"Previous version: {previous_version}")

    if current_version != previous_version and previous_version is not None:
        print("Version has changed")
        # 使用新的GitHub Actions输出方式
        if 'GITHUB_OUTPUT' in os.environ:
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                f.write(f"changed=true\n")
                f.write(f"new_version={current_version}\n")
                f.write(f"previous_version={previous_version}\n")
        else:
            # 非GitHub Actions环境下的输出（用于调试）
            print(f"::set-output name=changed::true")
            print(f"::set-output name=new_version::{current_version}")
            print(f"::set-output name=previous_version::{previous_version}")
        return True
    else:
        print("Version has not changed")
        # 使用新的GitHub Actions输出方式
        if 'GITHUB_OUTPUT' in os.environ:
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                f.write(f"changed=false\n")
                f.write(f"new_version=\n")
                f.write(f"previous_version=\n")
        else:
            # 非GitHub Actions环境下的输出（用于调试）
            print(f"::set-output name=changed::false")
            print(f"::set-output name=new_version::")
            print(f"::set-output name=previous_version::")
        return False


if __name__ == "__main__":
    import os
    main()