#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import datetime
import uuid
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phishing_sim.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ethical warning that must be acknowledged
ETHICAL_WARNING = """
THIS IS A SIMULATION TOOL FOR SECURITY AWARENESS TRAINING ONLY.
USE ONLY WITH EXPLICIT PERMISSION ON AUTHORIZED SYSTEMS.
UNAUTHORIZED USE MAY BE ILLEGAL.
"""

# Database Models
class Campaign(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    template = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    participants = db.relationship('Participant', backref='campaign', lazy=True)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.String(36), db.ForeignKey('campaign.id'), nullable=False)
    session_id = db.Column(db.String(36), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200)))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    credentials = db.relationship('Credential', backref='participant', lazy=True)

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))  # Hashed for ethical reasons
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Templates configuration
TEMPLATES = {
    'gmail': {
        'name': 'Gmail',
        'login_url': 'https://accounts.google.com',
        'logo': '/static/gmail-logo.png',
        'css': 'gmail.css'
    },
    'facebook': {
        'name': 'Facebook',
        'login_url': 'https://facebook.com',
        'logo': '/static/facebook-logo.png',
        'css': 'facebook.css'
    },
    'office365': {
        'name': 'Office 365',
        'login_url': 'https://office.microsoft.com',
        'logo': '/static/office365-logo.png',
        'css': 'office365.css'
    }
}

@app.before_request
def check_ethical_warning():
    if 'ethical_warning_accepted' not in session and request.endpoint not in ('ethical_warning', 'static'):
        return redirect(url_for('ethical_warning'))

@app.route('/ethical-warning', methods=['GET', 'POST'])
def ethical_warning():
    if request.method == 'POST':
        session['ethical_warning_accepted'] = True
        return redirect(url_for('admin_dashboard'))
    return render_template('ethical_warning.html', warning=ETHICAL_WARNING)

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_authenticated'):
        return redirect(url_for('admin_login'))
    campaigns = Campaign.query.all()
    return render_template('admin_dashboard.html', campaigns=campaigns)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == os.getenv('ADMIN_PASSWORD', 'training123'):
            session['admin_authenticated'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/create-campaign', methods=['POST'])
def create_campaign():
    if not session.get('admin_authenticated'):
        return redirect(url_for('admin_login'))
    
    campaign_id = str(uuid.uuid4())
    campaign = Campaign(
        id=campaign_id,
        name=request.form.get('name'),
        template=request.form.get('template')
    )
    db.session.add(campaign)
    db.session.commit()
    
    return redirect(url_for('campaign_details', campaign_id=campaign_id))

@app.route('/campaign/<campaign_id>')
def campaign_details(campaign_id):
    if not session.get('admin_authenticated'):
        return redirect(url_for('admin_login'))
    
    campaign = Campaign.query.get_or_404(campaign_id)
    participants = Participant.query.filter_by(campaign_id=campaign_id).all()
    return render_template('campaign_details.html', 
                         campaign=campaign,
                         participants=participants,
                         templates=TEMPLATES)

@app.route('/simulate/<template_name>')
def simulate_phishing(template_name):
    if template_name not in TEMPLATES:
        return "Invalid simulation template", 404
    
    # Create participant record
    participant = Participant(
        campaign_id=request.args.get('campaign', ''),
        session_id=str(uuid.uuid4()),
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(participant)
    db.session.commit()
    
    session['participant_id'] = participant.id
    return render_template(f'{template_name}.html', 
                         template=TEMPLATES[template_name])

@app.route('/submit-credentials', methods=['POST'])
def submit_credentials():
    if 'participant_id' not in session:
        return "Invalid session", 400
    
    # Store hashed credentials for ethical reasons
    credential = Credential(
        participant_id=session['participant_id'],
        username=request.form.get('username', ''),
        password=generate_password_hash(request.form.get('password', ''))
    )
    db.session.add(credential)
    db.session.commit()
    
    return render_template('simulation_complete.html')

@app.route('/participant/<participant_id>')
def participant_details(participant_id):
    if not session.get('admin_authenticated'):
        return redirect(url_for('admin_login'))
    
    participant = Participant.query.get_or_404(participant_id)
    credentials = Credential.query.filter_by(participant_id=participant_id).all()
    return render_template('participant_details.html',
                        participant=participant,
                        credentials=credentials)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Create default admin if not exists
    if not os.getenv('ADMIN_PASSWORD'):
        print("WARNING: Using default admin password. Set ADMIN_PASSWORD environment variable in production.")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
