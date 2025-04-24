Attacks Demonstrated
🔥 1. HTTP Flood (DoS)
File: http_flood.py

Description: Sends high-frequency GET requests with spoofed IPs using the X-Forwarded-For header to simulate a denial-of-service attack.

Impact: Overwhelms server sockets, eventually crashing the web service. You'll see socket exhaustion errors (WinError 10048) and the site becomes inaccessible.

💉 2. Stored Cross-Site Scripting (XSS)
File: cross_site_scripting_account.py + XSS_register_and_inject.py

Description:

Registers a fake patient account with malicious JavaScript in the first_name field.

When a doctor views this profile, a fake login popup appears (credential phishing).

Credentials are silently sent to an attacker endpoint.

Impact: Exfiltrates sensitive doctor credentials through client-side script execution.

Defense Mechanisms
✅ Activate Defenses

python enable_defense_and_run.py
This script applies the following defenses:

Rate Limiting with Flask-Limiter:

Limits each IP to 100 requests/minute and 10 requests/second

Uses a custom get_real_ip() function to detect spoofed headers

XSS Mitigation:

Removes | safe from template rendering to auto-escape user inputs

Waitress WSGI Server:

Improves concurrency handling and socket management under attack
