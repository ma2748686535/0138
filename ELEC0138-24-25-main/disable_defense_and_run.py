import shutil
import subprocess
from pathlib import Path


backup_path = Path("app/app_original.py")
app_path = Path("app/app.py")
template_backup = Path("app/templates/view_patient_profile_original.html")
template_path = Path("app/templates/view_patient_profile.html")


if backup_path.exists():
    shutil.copyfile(backup_path, app_path)
    print("✅ app.py restored")
else:
    print("⚠️  app_original.py not found")


if template_backup.exists():
    shutil.copyfile(template_backup, template_path)
    print("✅ view_patient_profile.html restored")
else:
    print("⚠️  view_patient_profile_original.html not found")

subprocess.run(["python", "app/app.py"])            