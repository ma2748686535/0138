# ELEC0138 Hospital Appointment System with Security Demo

A Flask-based web application for hospital appointment scheduling that demonstrates common web security vulnerabilities and defenses as part of the ELEC0138 module coursework.

## 🏥 Project Overview

This project implements a hospital appointment booking system with the following features:
- Patient registration and profile management
- Doctor accounts (by invitation only)
- Appointment scheduling and management
- Admin dashboard for doctor invitations

The system also includes demo attacks and defense mechanisms to illustrate common web security vulnerabilities.

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ELEC0138-24-25-main
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python -m app.app
```

## 🔐 Security Demonstrations

### Attack Vectors

#### 1. HTTP Flood (DoS)
**File:** `http_flood.py`

This script demonstrates a denial-of-service attack by sending high-frequency GET requests with spoofed IPs using the X-Forwarded-For header.

**Impact:** Overwhelms server sockets, eventually crashing the web service. You'll see socket exhaustion errors (WinError 10048) and the site becomes inaccessible.

#### 2. Stored Cross-Site Scripting (XSS)
**Files:** `cross_site_scripting_account.py` + `XSS_register_and_inject.py`

These scripts demonstrate a credential harvesting attack:
1. Registers a fake patient account with malicious JavaScript in the first_name field
2. When a doctor views this profile, a fake login popup appears (credential phishing)
3. Credentials are silently sent to an attacker endpoint

**Impact:** Exfiltrates sensitive doctor credentials through client-side script execution.

### Defense Mechanisms

Run the following command to enable all defense mechanisms:
```bash
python enable_defense_and_run.py
```

This script implements:

#### Rate Limiting with Flask-Limiter
- Limits each IP to 100 requests/minute and 10 requests/second
- Uses a custom `get_real_ip()` function to detect spoofed headers

#### XSS Mitigation
- Removes `| safe` from template rendering to auto-escape user inputs

#### Waitress WSGI Server
- Improves concurrency handling and socket management under attack

## 📂 Project Structure

- [`app/`](ELEC0138-24-25-main/app) - Main application code
  - [`app.py`](ELEC0138-24-25-main/app/app.py) - Core application logic
  - [`templates/`](ELEC0138-24-25-main/app/templates) - HTML templates
  - [`static/`](ELEC0138-24-25-main/app/static) - CSS, JavaScript, and other static files
- [`http_flood.py`](ELEC0138-24-25-main/http_flood.py) - DoS attack demonstration
- [`cross_site_scripting_account.py`](ELEC0138-24-25-main/cross_site_scripting_account.py) - XSS attack receiver
- [`XSS_register_and_inject.py`](ELEC0138-24-25-main/XSS_register_and_inject.py) - XSS attack payload injection
- [`enable_defense_and_run.py`](ELEC0138-24-25-main/enable_defense_and_run.py) - Security hardening script
- [`phishing_simulation/`](ELEC0138-24-25-main/phishing_simulation) - Contains tools for simulating phishing attacks
  - [`phishing_app.py`](ELEC0138-24-25-main/phishing_simulation/phishing_app.py) - Simulated phishing website
  - [`requirements.txt`](ELEC0138-24-25-main/phishing_simulation/requirements.txt) - Dependencies for the phishing simulation
- [`phishing_url_detector/`](ELEC0138-24-25-main/phishing_url_detector) - ML-based phishing URL detection tool
  - [`predict_helper.py`](ELEC0138-24-25-main/phishing_url_detector/predict_helper.py) - Helper module for phishing URL prediction
  - [`requirements.txt`](ELEC0138-24-25-main/phishing_url_detector/requirements.txt) - Dependencies for the phishing detector

## 🛠️ Technology Stack

- **Backend:** Flask, SQLAlchemy, Flask-Mail
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Security:** Werkzeug (password hashing), Flask-Limiter
- **Production Server:** Waitress WSGI

## 📄 License

[MIT License](LICENSE)

## 🤝 Contributing

This project is for educational purposes. If you'd like to contribute or suggest improvements, please open an issue or submit a pull request.
