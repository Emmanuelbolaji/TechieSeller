TechieSeller
TechieSeller is a Flask-based web application for an online marketplace specialized in tech products. It provides a platform for users to buy and sell various tech items.
Table of Contents

Introduction
Features
Project Structure
Installation
Usage
Database
Testing
Contributing
Related Projects
License

Introduction
TechieSeller aims to create a user-friendly platform for tech enthusiasts to trade their gadgets and accessories. Whether you're looking to upgrade your setup or find a new home for your gently used tech, TechieSeller has got you covered.

Deployed Site: TechieSeller Live
Project Blog Article: Building TechieSeller: A Journey in Flask and E-commerce
Author LinkedIn: Emmanuel Bolaji

Features

User authentication (register, login, logout)
Product listing and management
Shopping cart functionality
Secure payment integration with Paystack
Responsive design for various devices

Project Structure
CopyTechieSeller/
├── __pycache__/
├── instance/
│   └── market.db
├── market/
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   └── js/
│   └── templates/
├── migrations/
│   ├── versions/
│   ├── alembic.ini
│   ├── env.py
│   └── script.py.mako
├── test/
│   ├── test_forms.py
│   └── test_models.py
├── add_items.py
├── run.py
└── README.md
Installation

Clone the repository:
Copygit clone https://github.com/Emmanuelbolaji/TechieSeller.git
cd TechieSeller

Create a virtual environment and activate it:
Copypython -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required packages:
Copypip install -r requirements.txt

Set up the database:
Copyflask db upgrade

(Optional) Add sample items to the database:
Copypython add_items.py


Usage

Start the Flask development server:
Copypython run.py

Open a web browser and navigate to http://localhost:5000
Register a new account or log in with existing credentials
Browse the marketplace, add items to your cart, and complete purchases

Database
The application uses SQLite as the database, stored in instance/market.db. Database migrations are managed using Flask-Migrate and can be found in the migrations directory.
To create a new migration after modifying models:
Copyflask db migrate -m "Description of changes"
flask db upgrade
Testing
Run the tests using pytest:
Copypytest
Test files are located in the test directory and include:

test_forms.py: Tests for form validation
test_models.py: Tests for database models

Contributing
We welcome contributions to TechieSeller! Please follow these steps:

Fork the repository
Create a new branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

Please ensure your code adheres to our coding standards and includes appropriate tests.
Related Projects

TechBazaar - A similar marketplace for tech products built with Django
GadgetSwap - A peer-to-peer platform for exchanging tech gadgets

License
This project is licensed under the MIT License - see the LICENSE file for details.
