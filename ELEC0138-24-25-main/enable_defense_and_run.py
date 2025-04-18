import shutil
import subprocess
import time

source = "app/app.py"
backup = "app/app_original.py"

# 创建备份
shutil.copyfile(source, backup)

# 插入防御代码
with open(source, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "app = Flask(__name__)" in line:
        insert_index = i + 1
        limiter_code = """
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute", "10 per second"]
)
"""
        lines.insert(insert_index, limiter_code)
        break

for i, line in enumerate(lines):
    if "if __name__ == '__main__':" in line:
        lines[i] = "if __name__ == '__main__':\n"
        lines[i+1] = "    from waitress import serve\n    serve(app, host='127.0.0.1', port=5000, threads=8)\n"
        break

with open(source, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ 已添加限速防御并备份原始 app.py")

# 启动网站
print("🚀 正在启动网站...")
subprocess.run(["python", "app/app.py"])
