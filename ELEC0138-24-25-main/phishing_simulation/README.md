# Educational Phishing Simulation for Clinic Appointment System

## Overview

This project simulates a realistic phishing attack targeting users of a Clinic Appointment System. It demonstrates the techniques used by attackers to steal credentials through social engineering, website spoofing, and psychological manipulation. The simulation is designed for educational purposes to improve security awareness and defensive measures.

**IMPORTANT LEGAL DISCLAIMER: This simulation is strictly for educational and security training purposes only. Using these techniques against real systems or users without explicit permission is illegal and unethical.**

## Table of Contents

1. [Educational Purpose](#educational-purpose)
2. [Attack Simulation Components](#attack-simulation-components)
3. [Technical Implementation](#technical-implementation)
4. [Setup Instructions](#setup-instructions)
5. [How the Attack Works](#how-the-attack-works)
6. [Security Lessons](#security-lessons)
7. [Defensive Measures](#defensive-measures)
8. [Using This for Security Training](#using-this-for-security-training)
9. [Legal and Ethical Considerations](#legal-and-ethical-considerations)

## Educational Purpose

This simulation was developed to:

- Demonstrate real-world phishing techniques in a controlled environment
- Help security professionals understand attack vectors
- Train users to recognize phishing attempts
- Test defensive measures against credential theft
- Develop better security protocols for healthcare applications

## Attack Simulation Components

The simulation includes four main components:

1. **Fake Login Page**: A clone of the legitimate Clinic Appointment System login page with added elements designed to create urgency
2. **Phishing Email**: A template email with security alerts and a link to the fake page
3. **Credential Harvesting**: Server-side logging of submitted usernames and passwords
4. **Analytics**: Tracking of visitor data for educational analysis

## Technical Implementation

### Project Structure
```
phishing_simulation/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── logs/                  # Directory for captured credentials and analytics
│   ├── credentials.log    # Stores captured login credentials
│   └── visitors.log       # Tracks visitor information
│
├── static/                # Static assets
│   └── css/
│       └── style.css      # CSS styling for phishing pages
│
├── templates/             # HTML templates
│   ├── login.html         # Fake login page
│   └── redirect.html      # Success page after credential capture
│
└── phishing_email.html    # HTML template for phishing email
```

### Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Animation**: CSS animations for visual engagement
- **Logging**: File-based logging system
- **Tracking**: IP and user-agent tracking for educational purposes

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- Flask and Werkzeug packages

### Installation Steps

1. Clone the repository (for educational purposes only):
   ```bash
   git clone [repository-url]
   cd phishing_simulation
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the phishing simulation server:
   ```bash
   python app.py
   ```

5. Access the phishing page at http://localhost:5001/

### Usage Scenarios

- **For Classroom Demonstrations**: 
  Run on localhost and demonstrate how users can be tricked
  
- **For Security Awareness Training**:
  Set up on a controlled network with proper authorization
  
- **For Security Assessments**:
  Only use with explicit written permission as part of a formal security assessment

## How the Attack Works

### 1. Initial Contact via Phishing Email
- The attacker sends a convincing email about a security issue
- Email creates urgency with warnings about account expiration or security breach
- Contains a link to the fake login page (http://localhost:5001/login)

### 2. Spoofed Login Page
- Victim clicks the link and sees a page visually identical to the real system
- Page includes security alerts and warnings to create urgency
- Psychological manipulation techniques create pressure to act quickly

### 3. Credential Harvesting
- When the victim enters their username and password, data is sent to the attacker
- Credentials are logged on the server in `logs/credentials.log`
- User is unaware their information has been compromised

### 4. Seamless Redirection
- After submitting credentials, victim sees a success message
- The page appears to process verification successfully
- User is redirected to a legitimate-looking page, suspecting nothing

### 5. Credential Misuse (not implemented in this simulation)
- In a real attack, the captured credentials would be used to access the victim's account
- The attacker might steal personal information, make unauthorized changes, or perform actions as the victim

## Security Lessons

This simulation teaches several critical security lessons:

### For End Users
1. **URL Verification**: Always check the URL in your browser's address bar
   - Legitimate sites use HTTPS (look for the padlock)
   - Verify the domain matches exactly what you expect

2. **Skepticism of Urgency**: Be suspicious of messages creating artificial time pressure
   - Legitimate organizations rarely demand immediate action via email
   - Threats about account suspension are common phishing tactics

3. **Direct Navigation**: Type URLs directly or use bookmarks instead of clicking email links
   - When in doubt, open a new browser window and navigate directly to the service
   - Call the organization directly using a known, verified phone number

4. **Multi-factor Authentication (MFA)**: Use whenever possible
   - Even if credentials are stolen, MFA provides an additional layer of protection
   - Use authenticator apps rather than SMS where possible

### For Organizations
1. **Email Authentication**: Implement SPF, DKIM, and DMARC
2. **Security Headers**: Use Content-Security-Policy and other security headers
3. **User Training**: Regular phishing awareness training
4. **Incident Response**: Have a plan for credential theft incidents

## Defensive Measures

Organizations should implement these protective measures:

### Technical Controls
1. **HTTPS Enforcement**: Secure all web applications with valid SSL/TLS certificates
2. **Email Security**: 
   - SPF (Sender Policy Framework) to verify email sources
   - DKIM (DomainKeys Identified Mail) for email authentication
   - DMARC (Domain-based Message Authentication, Reporting & Conformance) policy
3. **Multi-factor Authentication**: Require MFA for all logins
4. **Web Application Firewall**: Filter suspicious requests
5. **Anti-Phishing Tools**: Email scanning and link verification
6. **HSTS**: HTTP Strict Transport Security headers

### Administrative Controls
1. **Security Awareness Training**: Regular phishing simulations and education
2. **Security Policies**: Clear guidelines for handling sensitive information
3. **Incident Response**: Procedures for credential theft incidents
4. **Access Reviews**: Regular review of access rights

### User Education
1. **Phishing Recognition Training**: Help users identify suspicious emails
2. **Reporting Procedures**: Clear process for reporting suspicious messages
3. **Password Management**: Education on using password managers
4. **Verification Procedures**: Training on verifying message authenticity

## Using This for Security Training

### Classroom Demonstrations
1. Run the simulation locally
2. Walk through each component explaining the techniques
3. Show how the phishing page differs from legitimate pages
4. Demonstrate credential logging

### Company-Wide Phishing Exercises
If using this for organizational training (with proper authorization):

1. Customize the templates to match your organization
2. Send controlled phishing emails to employees
3. Track who clicks links and submits credentials
4. Follow up with immediate education for those who fall victim
5. Share anonymized results and lessons learned

### Security Assessment Integration
For professional security assessments:

1. Include as part of authorized penetration testing
2. Document findings and recommend mitigations
3. Use results to improve security awareness training

## Legal and Ethical Considerations

### Legal Requirements
- **Authorization**: Never conduct phishing simulations without explicit written permission
- **Data Protection**: Handle any collected data according to applicable laws (GDPR, HIPAA, etc.)
- **Documentation**: Maintain documentation of authorization and testing scope

### Ethical Guidelines
- **Transparency**: Be clear about the educational purpose
- **No Harm**: Design simulations to educate, not embarrass
- **Privacy**: Respect privacy and confidentiality of participants
- **Proportionality**: Ensure the simulation is appropriate for the audience

### Disclaimer

This code is provided for educational and research purposes only. The creator assumes no liability and is not responsible for any misuse or damage caused by this program. Using phishing techniques against real systems or users without explicit permission is illegal and unethical.

---

Created for ELEC0138-24-25 Security Project 