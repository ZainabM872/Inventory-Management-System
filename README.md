# 🧾 CZAventory - Restaurant Inventory Management System

A user-friendly and low-cost **Inventory Management System (IMS)** designed for small-scale restaurants. This Django-based web application automates inventory tracking, order management, and implements role-based access to help restaurants streamline their operations and reduce manual errors.

---

## 📌 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Login Credentuals](#login-credentials)
---
## Features

- **Inventory Tracking:** Monitors real-time stock levels for all ingredients and items.
- **Order Management:** Automatically updates inventory based on new orders.
- **Stock Alerts:** Sends alerts when inventory items reach a low threshold.
- **User Access Control:** Role-based access for admins, managers, and staff.

---

## Tech Stack

- **Backend:** Django (Python)
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **Others:** Bootstrap, Django Admin, Unicons

---
## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL Server
- pip
- virtualenv (optional but recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/ZainabM872/Inventory-Management-System.git
cd Inventory-Management-System
```
### 2. Create and Activate Virtual Environment (optional)
```bash
python -m venv env
```
on Mac:
```bash
source env/bin/activate
```
on Windows:
```bash
env\Scripts\activate
```

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

### 4. Configure MySQL Database
#### A. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### B: Install MySQL
```bash
brew install mysql
```
- if you're using Windows, download the MySQL Installer from 'https://dev.mysql.com/downloads/installer/'

#### C: Start MySQL
```bash
brew services start mysql
```
- During setup, set a username and password and remember it.

#### D: Log into MySQL and Create a Database
```bash
mysql -u root -p
```
- on Windows, start the MySQL Server from the installer dashboard or as a service.


- Create a MySQL database named ims_db (or your preferred name).
```sql
CREATE DATABASE your_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```
- Update settings.py in the Django project with your MySQL credentials:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ims_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

```
### 5. Run Migrations
```bash
python manage.py makemigrations
```
Chose this option:
1) Provide a one-off default now which will be set on all existing rows.<br/>
Accept default timezone or provide another value.<br/>
```bash
python manage.py migrate
```

### 6. Load DB Data
```bash
python manage.py load_all_data
```
This will load all the data created in dashboard/management/commands
### 7. Create Superuser
```bash
python manage.py createsuperuser
```
- Follow the prompts to set a username and password.

### 8. Run the Development Server
```bash
python manage.py runserver
```
- Visit http://127.0.0.1:8000/ to view the app.

### 9. Login Credentials 
To access the system you will need to login with name and password stored in the db.
<br/>
**Manager Credentials**:
- name: Alisha
- password: alisha_password
**Staff Credentials**:
- name: Caio
- caio_password
<br/>
Obs: All of the db loaded data can be modified inside the dashboard/management/commands files. If you modify you will have to drop the database and repeat the steps from step 5.

