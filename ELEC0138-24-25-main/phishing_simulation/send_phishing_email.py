#!/usr/bin/env python3
"""
Phishing Simulation Email Sender Script

This script sends simulated phishing emails using customizable templates.
It integrates with the phishing URL detector to validate URLs in emails.
"""

import os
import sys
import smtplib
import argparse
import csv
import time
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import logging
import json

# Add the phishing_url_detector directory to the path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "phishing_url_detector"))
from predict_helper import predict_url_phishing_proba

# Setup logging
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, f"phishing_campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_template(template_name):
    """Load an email template from the templates directory."""
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "templates", 
        template_name
    )
    
    if not os.path.exists(template_path):
        # If template doesn't exist in templates folder, check if it exists in main directory
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), template_name)
    
    if not os.path.exists(template_path):
        logging.error(f"Template not found: {template_name}")
        raise FileNotFoundError(f"Template {template_name} not found")
        
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def personalize_email(template, recipient_data):
    """Replace placeholders in template with personalized data."""
    personalized = template
    for key, value in recipient_data.items():
        placeholder = f"{{{{{key}}}}}"
        personalized = personalized.replace(placeholder, str(value))
    return personalized

def validate_urls_in_template(template):
    """Extract and validate URLs in the template using the phishing detector."""
    import re
    url_pattern = r'href=[\'"]?([^\'" >]+)'
    urls = re.findall(url_pattern, template)
    
    url_risks = []
    for url in urls:
        try:
            risk_score = predict_url_phishing_proba(url, None, show_output=False)
            url_risks.append((url, risk_score))
            logging.info(f"URL: {url} - Phishing Risk Score: {risk_score:.3f}")
        except Exception as e:
            logging.error(f"Failed to analyze URL {url}: {str(e)}")
    
    return url_risks

def send_email(sender_email, sender_password, recipient_email, subject, html_content, smtp_server, smtp_port):
    """Send an email using SMTP."""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        logging.info(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email to {recipient_email}: {str(e)}")
        return False

def run_campaign(config_file):
    """Run a phishing campaign based on a configuration file."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Load email template
        template = load_template(config['template'])
        
        # Validate URLs in template
        url_risks = validate_urls_in_template(template)
        logging.info(f"URL Risk Analysis: {url_risks}")
        
        # Load recipients
        recipients = []
        with open(config['recipients_csv'], 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                recipients.append(row)
        
        # Send emails
        sent_count = 0
        for recipient in recipients:
            if config.get('randomize_delay', False):
                delay = random.randint(
                    config.get('min_delay_seconds', 5),
                    config.get('max_delay_seconds', 60)
                )
                time.sleep(delay)
            
            personalized_content = personalize_email(template, recipient)
            success = send_email(
                config['sender_email'],
                config['sender_password'],
                recipient['email'],
                config['subject'],
                personalized_content,
                config['smtp_server'],
                config['smtp_port']
            )
            
            if success:
                sent_count += 1
        
        logging.info(f"Campaign completed. Sent {sent_count}/{len(recipients)} emails.")
        print(f"Campaign completed. Sent {sent_count}/{len(recipients)} emails.")
        
    except Exception as e:
        logging.error(f"Campaign failed: {str(e)}")
        print(f"Campaign failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Send phishing simulation emails')
    parser.add_argument('config', help='Path to campaign configuration JSON file')
    args = parser.parse_args()
    
    run_campaign(args.config)

if __name__ == "__main__":
    main() 