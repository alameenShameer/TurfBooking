# 🏟️ TurfBooking – Refactored Django Project

TurfBooking is a Django-based web application for booking sports turfs.  
This repository contains a clean and refactored version of the project, intended for learning, collaboration, and future development.

## 🚀 Features
- User & Turf Owner authentication
- Turf listing by location
- Slot-based booking system
- Booking history (My Bookings)
- Turf Owner dashboard
- Admin management via Django Admin

## 🛠️ Tech Stack
- Backend: Django 4.2
- Database: MySQL
- Frontend: HTML, CSS (Django Templates)
- Python: 3.10+

## 📁 Project Structure
TurfBooking/
├── turffinal/          # Django project & apps  
├── requirements.txt    # Dependencies  
├── .gitignore  
└── README.md  

## ⚙️ Setup Instructions

### 1. Clone Repository
git clone https://github.com/<your-username>/TurfBooking.git  
cd TurfBooking  

### 2. Create Virtual Environment

Windows:
python -m venv venv  
venv\Scripts\activate  

macOS / Linux:
python3 -m venv venv  
source venv/bin/activate  

### 3. Install Dependencies
pip install -r requirements.txt  

## 🗄️ Database Configuration (MySQL)

Create database:
CREATE DATABASE gamevillage;

Update `settings.py`:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gamevillage',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

## 🔄 Run Project
python manage.py migrate  
python manage.py createsuperuser  
python manage.py runserver  

## 🌐 Access
App: http://127.0.0.1:8000/  
Admin: http://127.0.0.1:8000/admin/  

## 🤝 Contribution Rules
- Do NOT push venv/
- Do NOT push local database files
- Create feature branches for new work
- Update requirements.txt if dependencies change

## 📌 Notes
This project is intended for educational and academic use.  
Future updates will include UI improvements and additional features.

## 👨‍💻 Maintainer
Al Ameen  
Computer Science Engineering Student
