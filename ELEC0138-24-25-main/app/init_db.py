from app import app, db, User, PatientProfile, DoctorInvite
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import sys

def init_db():
    try:
        with app.app_context():
            # Clear existing data
            print("Dropping all existing tables...")
            db.drop_all()
            print("Creating new tables...")
            db.create_all()
            
            print("Creating users...")
            
            # Create admin
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            
            # Create doctors
            doctors = [
                {
                    'username': 'dr.smith',
                    'password': 'doctor123',
                    'specialization': 'Cardiology'
                },
                {
                    'username': 'dr.jones',
                    'password': 'doctor123',
                    'specialization': 'Pediatrics'
                },
                {
                    'username': 'dr.wilson',
                    'password': 'doctor123',
                    'specialization': 'Dermatology'
                }
            ]   
            
            for doctor in doctors:
                new_doctor = User(
                    username=doctor['username'],
                    password=generate_password_hash(doctor['password']),
                    role='doctor',
                    specialization=doctor['specialization']
                )
                db.session.add(new_doctor)
            
            # Create patients with profiles
            patients = [
                {
                    'username': 'patient1',
                    'password': 'patient123',
                    'profile': {
                        'first_name': 'John',
                        'last_name': 'Smith',
                        'phone': '020-1234-5678',
                        'date_of_birth': datetime(1990, 5, 15),
                        'gender': 'Male',
                        'blood_group': 'O+',
                        'allergies': 'Penicillin',
                        'medical_conditions': 'Asthma',
                        'current_medications': 'Ventolin inhaler',
                        'emergency_contact_name': 'Jane Smith',
                        'emergency_contact_phone': '123-456-7890'
                    }
                },
                {
                    'username': 'patient2',
                    'password': 'patient123',
                    'profile': {
                        'first_name': 'Sarah',
                        'last_name': 'Johnson',
                        'phone': '020-2345-6789',
                        'date_of_birth': datetime(1985, 8, 22),
                        'gender': 'Female',
                        'blood_group': 'A+',
                        'allergies': 'None',
                        'medical_conditions': 'Hypertension',
                        'current_medications': 'Lisinopril',
                        'emergency_contact_name': 'John Doe',
                        'emergency_contact_phone': '098-765-4321'
                    }
                },
                {
                    'username': 'patient3',
                    'password': 'patient123',
                    'profile': {
                        'first_name': 'Alex',
                        'last_name': 'Taylor',
                        'phone': '020-3456-7890',
                        'date_of_birth': datetime(1995, 3, 10),
                        'gender': 'Other',
                        'blood_group': 'B-',
                        'allergies': 'Pollen, Dust',
                        'medical_conditions': 'None',
                        'current_medications': 'None',
                        'emergency_contact_name': 'Mary Johnson',
                        'emergency_contact_phone': '555-123-4567'
                    }
                }
            ]
            
            print("Creating patient accounts and profiles...")
            for patient in patients:
                # Create patient user
                new_patient = User(
                    username=patient['username'],
                    password=generate_password_hash(patient['password']),
                    role='patient'
                )
                db.session.add(new_patient)
                db.session.flush()  # This will assign an ID to new_patient
                
                # Create patient profile
                profile = PatientProfile(
                    user_id=new_patient.id,
                    **patient['profile']
                )
                db.session.add(profile)
            
            # Create some doctor invite codes
            invite_codes = [
                DoctorInvite(
                    invite_code='DOC123',
                    email='newdoctor@example.com',
                    created_by='admin'
                ),
                DoctorInvite(
                    invite_code='DOC456',
                    created_by='admin'
                )
            ]
            
            for invite in invite_codes:
                db.session.add(invite)
            
            # Commit all changes
            print("Committing changes to database...")
            db.session.commit()
            
            # Verify the data was created
            print("\nVerifying database initialization...")
            admin_count = User.query.filter_by(role='admin').count()
            doctor_count = User.query.filter_by(role='doctor').count()
            patient_count = User.query.filter_by(role='patient').count()
            profile_count = PatientProfile.query.count()
            invite_count = DoctorInvite.query.count()
            
            print(f"Found {admin_count} admin(s)")
            print(f"Found {doctor_count} doctor(s)")
            print(f"Found {patient_count} patient(s)")
            print(f"Found {profile_count} patient profile(s)")
            print(f"Found {invite_count} doctor invite(s)")
            
            if admin_count == 1 and doctor_count == 3 and patient_count == 3 and profile_count == 3 and invite_count == 2:
                print("\nDatabase initialized successfully!")
                
                # Print credentials for testing
                print("\nTest Credentials:")
                print("-----------------")
                print("Admin:")
                print("Username: admin")
                print("Password: admin123")
                print("\nDoctors:")
                for doc in doctors:
                    print(f"Username: {doc['username']}")
                    print(f"Password: {doc['password']}")
                    print(f"Specialization: {doc['specialization']}")
                    print()
                print("\nPatients:")
                for pat in patients:
                    print(f"Username: {pat['username']}")
                    print(f"Password: {pat['password']}")
                    print()
            else:
                print("\nWarning: Database initialization may be incomplete!")
                print("Please check the counts above and verify the data manually.")
                
    except Exception as e:
        print(f"\nError initializing database: {str(e)}")
        db.session.rollback()
        sys.exit(1)

if __name__ == '__main__':
    init_db() 