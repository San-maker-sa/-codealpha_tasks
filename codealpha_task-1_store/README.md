# CodeAlpha Task 1 – Ice's Super Store

Simple Django e-commerce demo project.

## Features

- Product listing and detail pages
- Session-based cart (add / remove items)
- Checkout page with customer details form
- Cash on Delivery and Online (fake) payment options
- Order success page, My Orders list, and Order Detail page

## Tech stack

- Python 3
- Django
- Bootstrap 5
- SQLite (default Django database)

## How to run locally

1. Create and activate virtual environment (optional but recommended).
2. Install dependencies (Django):
   - `pip install django`
3. Apply migrations:
   - `python manage.py migrate`
4. Create superuser (optional, for admin):
   - `python manage.py createsuperuser`
5. Run development server:
   - `python manage.py runserver`
6. Open `http://127.0.0.1:8000/` in your browser.
