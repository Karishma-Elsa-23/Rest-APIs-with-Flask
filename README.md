# Store REST API

A RESTful API for managing stores, items, tags, and users, built with Flask, Flask-Smorest, SQLAlchemy, Flask-JWT-Extended, and Flask-Migrate.

## Features

- CRUD operations for stores, items, and tags
- User registration, login, and JWT-based authentication
- Tagging system for items
- JWT blocklist for secure logout
- Database migrations with Flask-Migrate
- SQLite database by default

## Setup

1. **Clone the repository**
   ```sh
   git clone git@github.com:Karishma-Elsa-23/Rest-APIs-with-Flask.git
   cd Rest-APIs-with-Flask
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```sh
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Start the server**
   ```sh
   flask run
   ```

## API Endpoints

- `/store` - Manage stores
- `/item` - Manage items
- `/tag` - Manage tags
- `/register` - Register a new user
- `/login` - Obtain JWT token
- `/logout` - Invalidate JWT token

## Environment Variables

- `DATABASE_URL` (optional): Set a custom database URI
- `JWT_SECRET_KEY`: Secret key for JWT authentication

## Development

- Swagger UI available at `/swagger-ui`
- Database file: `data.db` 

