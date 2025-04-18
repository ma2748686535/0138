# Smart Appointment Scheduler for Clinic

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Flask-based web application for managing clinic appointments, designed to streamline the appointment booking process for both patients and doctors.

## Table of Contents
- [Features](#features)
- [Technical Stack](#technical-stack)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Security Features](#security-features)
- [Contributing](#contributing)
- [License](#license)

## Features

### User Management
- **Role-based Access Control**
  - Patients: Can book appointments and manage their profile
  - Doctors: Can view and manage appointments, view patient profiles
  - Admin: Can manage doctor invitations and view all appointments

- **Authentication System**
  - Secure login and registration
  - Password hashing for security
  - Session management

### Appointment Management
- **Appointment Booking**
  - Patients can book appointments with available doctors
  - Support for both online and in-person consultations
  - Date and time selection
  - Doctor selection based on specialization

- **Appointment Processing**
  - Doctors can approve or reject appointments
  - Automatic email notifications for appointment status
  - Microsoft Teams meeting links for online consultations
  - Appointment cancellation functionality

### Patient Profile Management
- **Comprehensive Patient Information**
  - Basic Information: First name, last name, phone, date of birth, gender, blood group
  - Medical Information: Allergies, medical conditions, current medications
  - Emergency Contact: Name and phone number

### Doctor Management
- **Doctor Registration**
  - Secure invitation system for doctor registration
  - Specialization tracking
  - Admin-controlled invitation codes

## Technical Stack
- **Backend**: 
  - Flask (Python)
  - Python 3.9+
- **Database**: 
  - SQLite with SQLAlchemy ORM
  - Database file: `instance/appointments.db`
- **Email**: 
  - Flask-Mail for notifications
  - SMTP configuration required in app.py
- **Authentication**: 
  - Werkzeug security utilities
  - Session-based authentication
- **Frontend**: 
  - HTML5, CSS3
  - Bootstrap 5
  - Jinja2 templating
- **Video Conferencing**: 
  - Microsoft Teams integration
  - Requires Microsoft 365 account

## Setup and Installation

### Prerequisites
- Python 3.9 or higher
- Git
- Microsoft 365 account (for Teams integration)

### Installation Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/smart-appointment-scheduler.git
   cd smart-appointment-scheduler/app
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Linux/macOS:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Configure the application**
   - Copy `.env.example` to `.env` and update:
     - `SECRET_KEY`: Generate a secure key
     - `DATABASE_URI`: SQLite database path
     - `MAIL_*`: Email server settings
     - `TEAMS_CLIENT_ID`: Microsoft Teams app ID

5. **Initialize the database**
   ```bash
   python init_db.py
   ```
   This creates:
   - Admin user (admin/admin123)
   - Sample doctors and patients

6. **Run the application**
   ```bash
   python app.py
   ```
   Access at: http://localhost:5000

## API Documentation

### Authentication
- **Login**: `POST /login`
  - Required fields: `username`, `password`
- **Logout**: `GET /logout`
- **Register**: `POST /register`
  - Required fields: `username`, `email`, `password`, `role`

### Appointments
- **Book Appointment**: `POST /appointments`
  - Required fields: `doctor_id`, `date`, `time`, `type`
- **Get Appointments**: `GET /appointments`
- **Update Appointment**: `PUT /appointments/<id>`
  - Status: `approved`, `rejected`, `completed`

### Users
- **Get Profile**: `GET /profile`
- **Update Profile**: `PUT /profile`
- **List Doctors**: `GET /doctors`

## Usage

### Admin Setup
1. Login with default credentials:
   - Username: `admin`
   - Password: `admin123`
2. Navigate to Admin Dashboard
3. Generate doctor invitation codes
4. Manage system settings

### Doctor Registration
1. Request invitation code from admin
2. Register at `/register` with:
   - Invitation code
   - Specialization details
   - Professional information

### Patient Registration
1. Register at `/register`
2. Complete profile information:
   - Personal details
   - Medical history
   - Emergency contacts

### Appointment Booking
1. Login as patient
2. Navigate to Book Appointment
3. Select:
   - Consultation type (online/in-person)
   - Preferred doctor
   - Available time slot
4. Confirm booking

### Appointment Management
1. Login as doctor
2. View appointments dashboard
3. Approve/reject appointments
4. For online consultations:
   - Generate Teams meeting link
   - Send to patient via email

## Troubleshooting

### Common Issues
1. **Database not initializing**
   - Ensure SQLite has write permissions
   - Check `instance/` directory exists
   - Verify database URI in configuration

2. **Email not sending**
   - Check SMTP settings in `.env`
   - Verify less secure apps allowed (for Gmail)
   - Test with mailtrap.io for development

3. **Teams integration failing**
   - Verify Microsoft 365 account
   - Check Teams client ID in configuration
   - Ensure proper redirect URIs

4. **Login issues**
   - Reset admin password via database if needed
   - Check session cookie settings

## Security Features
- **Password Security**
  - BCrypt hashing
  - Minimum 8 character requirement
  - Complexity enforcement
- **Session Management**
  - Secure, HTTP-only cookies
  - Session timeout (30 minutes)
  - CSRF protection
- **Access Control**
  - Role-based permissions
  - Route-level authorization
  - Secure doctor invitation system
- **Data Protection**
  - SQL injection prevention
  - XSS protection
  - Input validation

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---
