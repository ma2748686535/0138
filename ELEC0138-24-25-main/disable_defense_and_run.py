import shutil
import os
import subprocess

source = "app/app_original.py"
target = "app/app.py"

if os.path.exists(source):
    shutil.copyfile(source, target)
    print("✅ 已恢复原始版本 app.py")
    print("🚀 正在启动网站...")
    subprocess.run(["python", "app/app.py"])
else:
    print("⚠️ 未找到备份文件 app_original.py，无法恢复")
