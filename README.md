# Phishing Simulation Framework

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Flask Version](https://img.shields.io/badge/flask-2.0%2B-lightgrey)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![Warning](https://img.shields.io/badge/WARNING-For%20Educational%20Purposes%20Only-red)](#)


A controlled environment for conducting authorized phishing simulations and security awareness training.

## Features

- 🎭 Multiple realistic login templates (Gmail, Facebook, Office365)
- 📊 Comprehensive logging and reporting dashboard
- 🔐 Ethical credential handling (hashed storage)
- ⚠️ Mandatory ethical warning system
- 📈 Campaign management and tracking

## Prerequisites

- Python 3.8+
- pip package manager

## Installation


#### Clone the repository
```
git clone https://github.com/yourusername/phishing-simulator.git
cd phishing-simulator
```

#### Install dependencies
```
pip install -r requirements.txt
```

## Configuration
```
1. Set admin password:
export ADMIN_PASSWORD=your_secure_password

2. Initialize database:
python phishing_simulator.py --init-db
```

## Usage

#### Starting the Server
```
python phishing_simulator.py
```

### Accessing the Admin Dashboard
1. Visit `http://localhost:5000/admin`
2. Login with your admin password

### Creating a Simulation Campaign

1. Navigate to the admin dashboard
2. Click "Create New Campaign"
3. Select a template (Gmail, Facebook, etc.)
4. Name your campaign (e.g., "Q3 Security Training")

### Running Simulations

Share the generated URL with participants:
http://your-server:5000/simulate/gmail?campaign=CAMPAIGN_ID

## Ethical Guidelines

❗ **This tool must only be used:**

- With explicit participant consent
- For authorized security awareness training
- In compliance with all applicable laws
- Never against non-consenting individuals

**Include clear warnings that this is a simulation.**

## File Structure
```csharp
phishing-simulator/
├── phishing_simulator.py    # Main application
├── requirements.txt         # Dependencies
├── templates/               # HTML templates
│   ├── admin/               # Admin interface
│   ├── simulations/         # Phishing templates
│   └── ethical_warning.html # Mandatory warning
├── static/                  # Static files
│   ├── css/                 # Stylesheets
│   └── images/              # Template logos
└── phishing_sim.db          # Database (created automatically)
```


## License

This project is licensed under the MIT License - see the [LICENSE](https://license/) file for details.

## Disclaimer

This tool is for **educational purposes only**. The developers assume no liability for any misuse of this software. Always obtain proper authorization before conducting any security testing.
