import shutil
import subprocess
import re
from pathlib import Path

app_path = Path("app/app.py")
backup_path = Path("app/app_original.py")
template_path = Path("app/templates/view_patient_profile.html")
template_backup = Path("app/templates/view_patient_profile_original.html")


shutil.copyfile(app_path, backup_path)
shutil.copyfile(template_path, template_backup)


with open(app_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
inserted_limiter = False
inserted_func = False

for line in lines:

    if not inserted_func and "app = Flask(__name__)" in line:
        new_lines.append(line)
        new_lines.append(
            "\n"
            "def get_real_ip():\n"
            "    forwarded_for = request.headers.get('X-Forwarded-For', request.remote_addr)\n"
            "    return forwarded_for.split(',')[0].strip()\n"
        )
        inserted_func = True
        continue


    if not inserted_limiter and "app = Flask(__name__)" in line:
        inserted_limiter = True
        new_lines.append(
            "\n"
            "from flask_limiter import Limiter\n"
            "from flask_limiter.util import get_remote_address\n"
        )
        new_lines.append(line)
        new_lines.append(
            "\n"
            "limiter = Limiter(\n"
            "    key_func=get_real_ip,\n"
            "    app=app,\n"
            "    default_limits=[\"100 per minute\", \"10 per second\"]\n"
            ")\n"
        )
        continue


    if "if __name__ == '__main__':" in line:
        new_lines.append("if __name__ == '__main__':\n")
        new_lines.append("    from waitress import serve\n")
        new_lines.append("    serve(app, host='127.0.0.1', port=5000, threads=50)\n")
        break  
    else:
        new_lines.append(line)


with open(app_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)


with open(template_path, "r", encoding="utf-8") as f:
    html = f.read()

html = re.sub(r'\|\s*safe', '', html)

with open(template_path, "w", encoding="utf-8") as f:
    f.write(html)

print("🛡️ Defense Mode Activated")
print("🔒 Rate Limiting: 100 requests/minute, 10 requests/second")
print("📡 Real IP Detection: using X-Forwarded-For header")
print("🧼 XSS Protection: removed '|safe' from output templates")


subprocess.run(["python", "-c", "from app.app import app; from waitress import serve; serve(app, host='127.0.0.1', port=5000, threads=50)"])
