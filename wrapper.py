"""
Fluid Memory Skill - OpenClaw Interface
将流体大脑封装为 OpenClaw 可调用的 Skill
"""
import sys
import os
import subprocess

# Conda Python 路径 (因为需要 chromadb)
PYTHON_PATH = r"C:\Users\41546\miniconda3\python.exe"
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "fluid_skill.py")

def execute(action, content="", query=""):
    cmd = [PYTHON_PATH, SCRIPT_PATH, action]
    
    if action == "remember" and content:
        cmd.extend(["--content", content])
    elif action == "recall" and query:
        cmd.extend(["--query", query])
    elif action == "forget" and content:
        cmd.extend(["--content", content])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

# OpenClaw 会调用这个文件
if __name__ == "__main__":
    # 简单的 CLI 接口
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    parser.add_argument("--content", default="")
    parser.add_argument("--query", default="")
    args = parser.parse_args()
    
    print(execute(args.action, args.content, args.query))
