import shutil
import os
import subprocess

source = "app/app_original.py"
target = "app/app.py"

if os.path.exists(source):
    shutil.copyfile(source, target)
    print("✅   The original version of app.py has been restored.")
    print("🚀 The website is starting up...")
    subprocess.run(["python", "app/app.py"])
else:
    print("⚠️ The backup file app_original.py was not found and cannot be restored.")
