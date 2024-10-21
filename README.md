# GreatKart - E-commerce Project

GreatKart is an e-commerce platform built with Python and Django. It includes features like a cart system, checkout, orders, payment integration (with PayPal Sandbox), dashboard, and email authentication with tokens.

## Features

- User Registration & Authentication
- Product Search and Filtering
- Add to Cart
- Checkout and Payment Integration (PayPal Sandbox)
- Order Management
- Admin Dashboard
- Email Confirmation with Tokens

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Django 4.x
- pip (Python package manager)
- Virtual environment (optional but recommended)

## Setting up the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/greatkart.git
cd greatkart
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv 
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

```bash
python manage.py migrate
```
### 5. Run the Development Server

```bash
python manage.py runserver
```
The application should now be accessible at `http://127.0.0.1:8000/`.
------------------------------------------------------------------------
