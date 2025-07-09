# Ecommerce API

A robust, production-ready ecommerce backend built with Django and Django REST Framework. This project supports user authentication, product management, order processing, comments, likes, tags, and background email notifications. It is ready for deployment on platforms like Liara and supports scalable, asynchronous task processing with Celery.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Setup](#database-setup)
  - [Running the Project](#running-the-project)
  - [Celery Worker](#celery-worker)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Management Commands](#management-commands)
- [Deployment](#deployment)
- [License](#license)

---

## Features

- **User Authentication** (JWT, Djoser)
- **Product Catalog** (CRUD, categories, images, discounts)
- **Shopping Cart** (add/remove items, checkout)
- **Order Management** (status tracking, admin/customer views)
- **Comments & Reviews** (approval workflow)
- **Likes & Tags** (generic relations)
- **Email Notifications** (Celery, templated emails)
- **API Documentation** (Swagger/OpenAPI)
- **Admin Panel** (customized)
- **Sample Data Generation** (factories, management commands)
- **Testing** (pytest, model_bakery)
- **Ready for Production** (Gunicorn, Whitenoise, Liara config)

---

## Tech Stack

- **Python 3.12**
- **Django 5.1**
- **Django REST Framework**
- **Celery & Redis** (background tasks)
- **MySQL** (default DB, configurable)
- **Djoser** (auth endpoints)
- **drf-yasg & drf-spectacular** (API docs)
- **pytest** (testing)
- **Liara** (deployment-ready)

---

## Project Structure

```
ecommerce/
  config/           # Django settings, URLs, WSGI/ASGI
  core/             # Custom user model, base app
  store/            # Products, categories, orders, carts, comments, images
  emailbackend/     # Email sending, Celery tasks
  likes/            # Generic like system
  tags/             # Generic tagging system
  static/           # Static files
  media/            # Uploaded media
  templates/        # HTML templates
  requirements.txt  # Python dependencies
  Pipfile           # Pipenv dependencies
  Procfile          # Gunicorn entrypoint
  liara.json        # Liara deployment config
```

---

## Getting Started

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ecommerce
   ```

2. **Install dependencies:**
   - Using pip:
     ```bash
     pip install -r requirements.txt
     ```
   - Or with pipenv:
     ```bash
     pipenv install --dev
     ```

3. **Set up environment variables:**
   - Copy and edit as needed:
     ```
     cp .env.example .env
     ```
   - Or configure via `liara.json` for Liara deployment.

### Database Setup

- Default: MySQL (see `liara.json` for config)
- For local development, you can use SQLite by changing `DATABASES` in `config/settings/dev.py`.

- **Apply migrations:**
  ```bash
  python manage.py migrate
  ```

- **Create a superuser:**
  ```bash
  python manage.py createsuperuser
  ```

### Running the Project

- **Development server:**
  ```bash
  python manage.py runserver
  ```

- **Production (Gunicorn):**
  ```bash
  gunicorn config.wsgi
  ```

### Celery Worker

- **Start Celery worker:**
  ```bash
  celery -A config worker --loglevel=info
  ```
- **Start Celery beat (for scheduled tasks):**
  ```bash
  celery -A config beat --loglevel=info
  ```

---

## API Documentation

- **Swagger UI:**  
  [http://localhost:8000/store/schema/docs](http://localhost:8000/store/schema/docs)

- **OpenAPI schema:**  
  [http://localhost:8000/store/schema/](http://localhost:8000/store/schema/)

- **Authentication:**  
  JWT via `/auth/jwt/create/`, `/auth/jwt/refresh/`, etc. (Djoser)

---

## Main API Endpoints

- `/store/products/` - Product CRUD, filtering, images, comments
- `/store/categories/` - Category CRUD
- `/store/customers/` - Customer info (admin/me)
- `/store/carts/` - Shopping cart management
- `/store/orders/` - Order management
- `/auth/` - User registration, login, JWT (Djoser)
- `/email/` - Email sending (triggers Celery task)
- `/admin/` - Django admin panel

---

## Management Commands

- **Generate sample data:**
  ```bash
  python manage.py generate_data --categories 10 --products 1000 --discounts 100 --comments-per-product 20
  ```

- **Truncate all tables:**
  ```bash
  python manage.py truncate_tables
  ```

---

## Testing

- **Run all tests:**
  ```bash
  pytest
  ```

- **Test config:**  
  See `pytest.ini` (uses `config.settings.dev`).

- **Fixtures:**  
  See `store/tests/conftest.py` for API client and authentication helpers.

---

## Deployment

- **Liara:**  
  Project is ready for [Liara](https://liara.ir/) deployment. See `liara.json` for configuration.

- **Static & Media:**  
  - Static files: `/static/`
  - Media files: `/media/`

- **Procfile:**  
  ```
  web: gunicorn config.wsgi --log-file -
  ```

---

## License

This project is licensed under the BSD License.

---

## Contact

For questions or support, please open an issue or contact the maintainer at `contact@myapi.local`.

---

**Happy coding!** 