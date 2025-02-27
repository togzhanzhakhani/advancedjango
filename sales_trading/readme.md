# 1. Clone the Repository
```sh
git clone https://github.com/togzhanzhakhani/advancedjango/sales_trading
cd sales_trading
```

# 2. Copy Environment Variables
```sh
cp env_ex .env
```

# 3. Start the Project
```sh
docker-compose up --build -d
```

# 4. Run migrations
```sh
docker-compose exec web python manage.py migrate
```

# API Documentation
### Once the server is running, access the API documentation at:
- `http://127.0.0.1:8000/docs/`

# Create a Superuser (Admin Access)

```sh
docker-compose exec web python manage.py createsuperuser
```

# Access the Admin Panel
### Login to the admin panel with your superuser credentials:
- `http://127.0.0.1:8000/admin/`

## Features
### Background Tasks with Celery:
- Trade Notifications: Email notifications for trade execution are processed asynchronously.
- Celery & Redis are integrated to handle background tasks.
### Trading Module: Order placement, order history, real-time order book management.
### Admin Panel: Manage categories, products, orders, invoices, discounts, and reports.
### API Documentation: Interactive API docs available at `/docs/`.
