## Video uploaded to YouTube: https://youtu.be/r8P7BT3YBUE

# API Documentation
### Once the server is running, access the API documentation at:
- `http://127.0.0.1:8000/docs/`

# Create a Superuser (Admin Access)

```sh
python manage.py createsuperuser
```

# Access the Admin Panel
### Login to the admin panel with your superuser credentials:
- `http://127.0.0.1:8000/admin/`

## Features
### Background Tasks with Celery:
- Email messages for trade execution are processed asynchronously.
- Celery & Redis are integrated to handle background tasks.
### Admin Panel: Manage categories, products, orders, invoices, discounts, and reports.
### API Documentation: Interactive API docs available at `/docs/`.
