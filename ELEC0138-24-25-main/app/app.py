"""Smart Appointment Scheduler for Clinic.

This module implements a Flask-based web application for managing clinic appointments.
It includes functionality for patient registration, appointment booking, and doctor management.
"""

from datetime import datetime, timedelta
import random
import string

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP server
app.config['MAIL_PORT'] = 587                 # Port for sending emails
app.config['MAIL_USE_TLS'] = True             # Use TLS encryption
app.config['MAIL_USERNAME'] = 'yuanzhehu2024@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = 'osml rhlm ookm fmrm'     
app.config['MAIL_DEFAULT_SENDER'] = 'yuanzhehu2024@gmail.com'  

db = SQLAlchemy(app)
mail = Mail(app)


class User(db.Model):
    """User model for storing user information.

    Attributes:
        id: Primary key for the user.
        username: Unique username for login.
        password: Hashed password for security.
        role: User role (patient, doctor, or admin).
        specialization: Doctor's specialization (only for doctors).
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False) 
    specialization = db.Column(db.String(100), nullable=True)  # Only for doctors


class Appointment(db.Model):
    """Appointment model for storing appointment information.

    Attributes:
        id: Primary key for the appointment.
        patient_name: Name of the patient.
        patient_email: Email of the patient.
        doctor_name: Name of the doctor.
        date: Date of the appointment.
        time: Time of the appointment.
        status: Current status of the appointment.
        consultation_type: Type of consultation (Online/Offline).
        meet_link: Google Meet link for online consultations.
    """
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_email = db.Column(db.String(100), nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="Pending")
    consultation_type = db.Column(db.String(20), nullable=False)
    meet_link = db.Column(db.String(200))  # For online consultations


class DoctorInvite(db.Model):
    """Doctor invitation model for managing doctor registration.

    Attributes:
        id: Primary key for the invitation.
        invite_code: Unique invitation code.
        email: Target email for the invitation.
        is_used: Whether the invitation has been used.
        created_at: When the invitation was created.
        created_by: Admin who created the invitation.
    """
    id = db.Column(db.Integer, primary_key=True)
    invite_code = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=True)  # Target email (optional)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(100), nullable=True)  # Admin who created it


class PatientProfile(db.Model):
    """Patient profile model for storing patient information.

    Attributes:
        id: Primary key for the profile.
        user_id: Foreign key to the User model.
        first_name: Patient's first name.
        last_name: Patient's last name.
        phone: Patient's phone number.
        date_of_birth: Patient's date of birth.
        gender: Patient's gender.
        blood_group: Patient's blood group.
        allergies: Patient's allergies.
        medical_conditions: Patient's medical conditions.
        current_medications: Patient's current medications.
        emergency_contact_name: Name of emergency contact.
        emergency_contact_phone: Phone of emergency contact.
        created_at: When the profile was created.
        updated_at: When the profile was last updated.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Basic Information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_group = db.Column(db.String(5))
    
    # Medical Information
    allergies = db.Column(db.Text)
    medical_conditions = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    
    # Emergency Contact
    emergency_contact_name = db.Column(db.String(100), nullable=False)
    emergency_contact_phone = db.Column(db.String(20), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)


def generate_invite_code(length=10):
    """Generates a random invitation code for doctor registration.

    Args:
        length: Length of the invitation code (default: 10).

    Returns:
        A random string of uppercase letters and digits.
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_meet_link():
    """Generates a Microsoft Teams meeting link for online consultations.

    Returns:
        A string containing a Microsoft Teams meeting URL.
    """
    # Teams meeting links typically follow this format:
    # https://teams.microsoft.com/l/meetup-join/19:meeting_ID@thread.tacv2/...
    # We'll generate a random meeting ID
    meeting_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
    return f"https://teams.microsoft.com/l/meetup-join/19:{meeting_id}@thread.tacv2"


# Initialize Database
with app.app_context():
    db.create_all()
    
    # Check if admin exists, if not, create one
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin_password = generate_password_hash('admin123')  # Change in production!
        admin_user = User(username='admin', password=admin_password, role='admin')
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created!")


@app.route('/')
def home():
    """Home page route.

    Returns:
        Rendered template for the home page with appointments and user role.
    """
    if 'user' in session:
        role = session['role']
        username = session['user']
        has_profile = False

        # Get the user first and verify it exists
        user = User.query.filter_by(username=username).first()
        if not user:
            # If user doesn't exist in database but exists in session, clear session
            session.clear()
            flash('User account not found. Please login again.', 'danger')
            return redirect(url_for('login'))

        if role == "patient":
            # Check if patient has completed profile
            profile = PatientProfile.query.filter_by(user_id=user.id).first()
            has_profile = profile is not None
            appointments = Appointment.query.filter_by(patient_name=username).all()
        elif role == "doctor":
            appointments = Appointment.query.filter_by(doctor_name=username).all()
        else:
            appointments = Appointment.query.all()  # For admins

        return render_template('index.html', appointments=appointments, 
                            role=role, has_profile=has_profile)

    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route.

    Returns:
        Rendered template for registration page or redirects to login on success.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        
        # Doctor role validation
        if role == "doctor":
            invite_code = request.form.get('invite_code')
            if not invite_code:
                flash('Invitation code required for doctor registration', 'danger')
                return redirect(url_for('register'))
                
            invite = DoctorInvite.query.filter_by(invite_code=invite_code, 
                                                is_used=False).first()
            if not invite:
                flash('Invalid or expired invitation code', 'danger')
                return redirect(url_for('register'))
            
            # Mark invitation as used
            invite.is_used = True
            specialization = request.form['specialization']
        else:
            specialization = None

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=password, role=role, 
                       specialization=specialization)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/doctor_dashboard')
def doctor_dashboard():
    """Doctor dashboard route.

    Returns:
        Rendered template for doctor dashboard with appointments.
    """
    if 'user' not in session or session['role'] != 'doctor':
        flash('Access denied. Only doctors can view this page.', 'danger')
        return redirect(url_for('login'))

    doctor_name = session['user']
    appointments = Appointment.query.filter_by(doctor_name=doctor_name).all()

    return render_template('doctor_dashboard.html', appointments=appointments)


@app.route('/approve_appointment/<int:id>')
def approve_appointment(id):
    """Route for approving appointments.

    Args:
        id: The ID of the appointment to approve.

    Returns:
        Redirects to doctor dashboard after approval.
    """
    if 'user' not in session or session['role'] != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    appointment = Appointment.query.get(id)
    if appointment:
        appointment.status = "Approved"

        if appointment.consultation_type == "Online":
            appointment.meet_link = generate_meet_link()  # Only for online consultations
            subject = "Your Online Consultation is Approved! ✅"
            body = (f"Dear {appointment.patient_name},\n\n"
                   f"Your online appointment with Dr. {appointment.doctor_name} "
                   f"has been approved.\n\n"
                   f"Join your consultation using this Microsoft Teams link: {appointment.meet_link}\n\n"
                   f"Thank you!")
        else:
            subject = "Your In-Person Appointment is Approved! ✅"
            body = (f"Dear {appointment.patient_name},\n\n"
                   f"Your in-person appointment with Dr. {appointment.doctor_name} "
                   f"is confirmed. Please visit the clinic on {appointment.date} "
                   f"at {appointment.time}.\n\nThank you!")

        db.session.commit()

        # Send email confirmation
        msg = Message(subject, recipients=[appointment.patient_email])
        msg.body = body
        mail.send(msg)

        flash('Appointment approved and email sent!', 'success')

    return redirect(url_for('doctor_dashboard'))


@app.route('/reject_appointment/<int:id>')
def reject_appointment(id):
    """Route for rejecting appointments.

    Args:
        id: The ID of the appointment to reject.

    Returns:
        Redirects to doctor dashboard after rejection.
    """
    if 'user' not in session or session['role'] != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    appointment = Appointment.query.get(id)
    if appointment:
        appointment.status = "Rejected"
        db.session.commit()

        # Send rejection email
        subject = "Your Appointment has been Rejected ❌"
        body = (f"Dear {appointment.patient_name},\n\n"
               f"Unfortunately, your appointment with Dr. {appointment.doctor_name} "
               f"on {appointment.date} at {appointment.time} has been rejected.\n\n"
               f"Please try booking another time.\n\nThank you!")

        msg = Message(subject, recipients=[appointment.patient_email])
        msg.body = body
        mail.send(msg)

        flash('Appointment rejected and email sent!', 'danger')

    return redirect(url_for('doctor_dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route.

    Returns:
        Rendered template for login page or redirects to home on success.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            session['role'] = user.role
            return redirect(url_for('home'))

        flash('Invalid credentials', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/book', methods=['GET', 'POST'])
def book_appointment():
    """Appointment booking route.

    Returns:
        Rendered template for booking page or redirects to home on success.
    """
    if 'user' not in session:
        flash('You must be logged in to book an appointment.', 'danger')
        return redirect(url_for('login'))
        
    # Check if user has completed their profile
    user = User.query.filter_by(username=session['user']).first()
    profile = PatientProfile.query.filter_by(user_id=user.id).first()
    
    if not profile:
        flash('Please complete your profile before booking an appointment.', 'warning')
        return redirect(url_for('patient_profile'))

    if request.method == 'POST':
        email = request.form['email']
        doctor_name = request.form['doctor_name']
        date = request.form['date']
        time = request.form['time']
        consultation_type = request.form['consultation_type']

        new_appointment = Appointment(
            patient_name=session['user'],
            patient_email=email,
            doctor_name=doctor_name,
            date=date,
            time=time,
            status="Pending",
            consultation_type=consultation_type
        )
        db.session.add(new_appointment)
        db.session.commit()

        flash('Appointment booked successfully! Waiting for doctor approval.', 
              'success')
        return redirect(url_for('home'))

    doctors = User.query.filter_by(role='doctor').all()
    return render_template('book.html', doctors=doctors)


@app.route('/cancel/<int:id>')
def cancel(id):
    """Appointment cancellation route.

    Args:
        id: The ID of the appointment to cancel.

    Returns:
        Redirects to home page after cancellation.
    """
    if 'user' not in session:
        flash('You must be logged in to cancel an appointment.', 'danger')
        return redirect(url_for('login'))

    appointment = Appointment.query.get(id)

    if not appointment:
        flash('Appointment not found!', 'danger')
        return redirect(url_for('home'))

    if (session['role'] == 'patient' and 
        appointment.patient_name != session['user']):
        flash('You can only cancel your own appointments!', 'danger')
        return redirect(url_for('home'))

    if (session['role'] == 'doctor' and 
        appointment.doctor_name != session['user']):
        flash('You can only cancel your own appointments!', 'danger')
        return redirect(url_for('home'))

    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment canceled successfully!', 'success')
    
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    """User logout route.

    Returns:
        Redirects to login page after clearing session.
    """
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('login'))


@app.route('/admin/invites', methods=['GET', 'POST'])
def admin_invites():
    """Admin route for managing doctor invitations.

    Returns:
        Rendered template for invitation management page.
    """
    # Check if user is admin
    if 'user' not in session or session.get('role') != 'admin':
        flash('Access denied. Only admins can access this page.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Generate new invite code
        email = request.form.get('email', '')
        new_code = generate_invite_code()
        invite = DoctorInvite(
            invite_code=new_code, 
            email=email,
            created_by=session['user'],
            created_at=datetime.utcnow()
        )
        db.session.add(invite)
        db.session.commit()
        
        # Optionally send email with invite code
        if email:
            subject = "Doctor Registration Invitation"
            body = f"You've been invited to register as a doctor. Use this invitation code: {new_code}"
            msg = Message(subject, recipients=[email])
            msg.body = body
            mail.send(msg)
            flash(f'Invitation sent to {email}', 'success')
        else:
            flash(f'New invitation code created: {new_code}', 'success')
    
    # Get all invite codes
    invites = DoctorInvite.query.order_by(DoctorInvite.created_at.desc()).all()
    return render_template('admin_invites.html', invites=invites)


@app.route('/profile', methods=['GET', 'POST'])
def patient_profile():
    """Patient profile management route.

    Returns:
        Rendered template for profile page or redirects to profile on success.
    """
    if 'user' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
        
    user = User.query.filter_by(username=session['user']).first()
    profile = PatientProfile.query.filter_by(user_id=user.id).first()
    
    if request.method == 'POST':
        if not profile:
            profile = PatientProfile(user_id=user.id)
            
        # Basic Information
        profile.first_name = request.form['first_name']
        profile.last_name = request.form['last_name']
        profile.phone = request.form['phone']
        profile.date_of_birth = datetime.strptime(request.form['date_of_birth'], 
                                                '%Y-%m-%d')
        profile.gender = request.form['gender']
        profile.blood_group = request.form['blood_group']
        
        # Medical Information
        profile.allergies = request.form['allergies']
        profile.medical_conditions = request.form['medical_conditions']
        profile.current_medications = request.form['current_medications']
        
        # Emergency Contact
        profile.emergency_contact_name = request.form['emergency_contact_name']
        profile.emergency_contact_phone = request.form['emergency_contact_phone']
        
        db.session.add(profile)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('patient_profile'))
        
    return render_template('profile.html', profile=profile)


@app.route('/view_patient_profile/<username>')
def view_patient_profile(username):
    """Route for doctors to view patient profiles.

    Args:
        username: The username of the patient whose profile to view.

    Returns:
        Rendered template for viewing patient profile.
    """
    if 'user' not in session or session['role'] != 'doctor':
        flash('Access denied. Only doctors can view patient profiles.', 'danger')
        return redirect(url_for('home'))
        
    patient = User.query.filter_by(username=username, role='patient').first()
    if not patient:
        flash('Patient not found.', 'danger')
        return redirect(url_for('doctor_dashboard'))
        
    profile = PatientProfile.query.filter_by(user_id=patient.id).first()
    if not profile:
        flash('Patient profile not found.', 'warning')
        return redirect(url_for('doctor_dashboard'))
        
    return render_template('view_patient_profile.html', profile=profile)


@app.context_processor
def utility_processor():
    """Adds utility functions to template context.

    Returns:
        Dictionary containing utility functions.
    """
    def get_db():
        return db
    return dict(get_db=get_db)



if __name__ == '__main__':
     app.run(debug=True)
    