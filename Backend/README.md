# Task Management Backend

FastAPI backend for the Task Management System.

## Features

- User authentication (signup/login/logout)
- JWT token-based security
- Task CRUD operations
- User-specific task management
- Input validation
- Comprehensive test suite

## Quick Start

```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
source env/bin/activate      # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
cd TaskApp
uvicorn main:app --reload --port 8000
```

## API Endpoints

### Authentication
- `POST /auth/signup` - Create new user
- `POST /auth/login` - Login (returns JWT token)
- `POST /auth/logout` - Logout

### Tasks (Authenticated)
- `GET /tasks/` - Get all user tasks
- `POST /tasks/` - Create task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task

## Testing

Run all tests:
```bash
cd TaskApp
PYTHONPATH=. pytest test/ -v
```

Run specific test file:
```bash
PYTHONPATH=. pytest test/test_auth.py -v
PYTHONPATH=. pytest test/test_tasks.py -v
```

**Windows users:**
```bash
# Command Prompt
set PYTHONPATH=.
pytest test/ -v

# PowerShell
$env:PYTHONPATH="."
pytest test/ -v
```

## Database

### Option 1: SQLite (Default - No Setup)
The app uses SQLite by default. The database file `tasks.db` is created automatically.

### Option 2: PostgreSQL (Recommended for Production)

1. **Create Database in pgAdmin:**
   - Open pgAdmin
   - Right-click on "Databases" → "Create" → "Database"
   - Name it `taskdb` → Click "Save"

2. **Set Environment Variable:**
   ```bash
   # Linux/Mac
   export DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@localhost:5432/taskdb"
   
   # Windows (Command Prompt)
   set DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/taskdb
   
   # Windows (PowerShell)
   $env:DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@localhost:5432/taskdb"
   ```

3. **Run the App:**
   ```bash
   cd TaskApp
   uvicorn main:app --reload --port 8000
   ```
   Tables are created automatically on first run!

## Tech Stack

- FastAPI
- SQLAlchemy ORM
- JWT (python-jose)
- Bcrypt (passlib)
- Pytest
