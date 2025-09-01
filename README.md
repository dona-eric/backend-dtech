# Backend (Django)

This backend is implemented using Django + Django REST Framework. Steps to run locally:

1. Create and activate venv
   python3 -m venv venv
   source venv/bin/activate

2. Install requirements
   ./venv/bin/pip install -r requirements.txt

3. Copy .env.example to .env and edit DATABASE_URL
   cp .env.example .env

4. Run migrations and start server
   ./venv/bin/python manage.py migrate
   ./venv/bin/python manage.py runserver 0.0.0.0:8000
