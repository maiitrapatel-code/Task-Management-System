# Task Management System

A full-stack task management application built with FastAPI (backend) and React (frontend).

## Quick Start (For Reviewers)

### Prerequisites
- Python 3.10+ installed
- Node.js 18+ installed
- PostgreSQL installed (with pgAdmin) OR use SQLite (no setup)

### 1. Database Setup (PostgreSQL with pgAdmin)
1. Open **pgAdmin**
2. Right-click "Databases" → "Create" → "Database"
3. Name: `taskdb` → Click "Save"

### 2. Clone and Setup Backend
```bash
cd Backend
python -m venv env
source env/bin/activate      # On Windows: env\Scripts\activate
pip install -r requirements.txt

# Set database connection (replace YOUR_PASSWORD with your PostgreSQL password)
export DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@localhost:5432/taskdb"

# On Windows use: set DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/taskdb

cd TaskApp
uvicorn main:app --reload --port 8000
```
Backend runs at: http://localhost:8000

> **Note:** Skip the DATABASE_URL step to use SQLite instead (no setup required)

### 3. Setup Frontend (new terminal)
```bash
cd Frontend
npm install
npm start
```
Frontend runs at: http://localhost:3000

### 4. Use the App
1. Open http://localhost:3000
2. Click "Sign up here" to create an account
3. Login and start managing tasks!

---

## Overview

This application allows users to:
- Create an account and login securely
- Create, view, update, and delete tasks
- Set task priorities (1-5)
- Mark tasks as complete/incomplete
- View all their personal tasks in an organized dashboard

## Project Structure

```
Assessment/
├── Backend/          # FastAPI backend
├── Frontend/         # React frontend
└── README.md         # This file
```

## Backend (FastAPI)

### Technologies Used
- Python 3.10+
- FastAPI
- SQLite (default, no setup needed) / PostgreSQL (optional)
- JWT Authentication
- Bcrypt for password hashing
- Pytest for testing

### Setup Instructions

1. Navigate to Backend directory:
```bash
cd Backend
```

2. Activate virtual environment:
```bash
source env/bin/activate
```

3. Install dependencies (already installed):
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
cd TaskApp
uvicorn main:app --reload --port 8000
```

The backend API will be available at: http://localhost:8000

### API Documentation
Once running, view the interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
cd Backend/TaskApp
pytest test/ -v
```

### API Endpoints

#### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout

#### Tasks (Protected)
- `GET /tasks/` - Get all user's tasks
- `POST /tasks/` - Create new task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task

## Frontend (React)

### Technologies Used
- React 18
- React Router for navigation
- Axios for API calls
- Context API for state management
- CSS3 for styling

### Setup Instructions

1. Navigate to Frontend directory:
```bash
cd Frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

The frontend will be available at: http://localhost:3000

### Features
- User registration with validation
- Secure login with JWT
- Dashboard with task grid layout
- Create/Edit tasks with modal
- Priority badges (color-coded)
- Responsive design
- Auto-logout on token expiration

## How to Use

1. **Start the Backend**:
   - Open terminal
   - Navigate to `Backend/TaskApp`
   - Activate env: `source ../env/bin/activate`
   - Run: `uvicorn main:app --reload --port 8000`

2. **Start the Frontend**:
   - Open new terminal
   - Navigate to `Frontend`
   - Run: `npm start`

3. **Use the Application**:
   - Visit http://localhost:3000
   - Sign up for a new account
   - Login with your credentials
   - Start managing your tasks!

## Testing

### Backend Tests
```bash
cd Backend/TaskApp
pytest test/ -v
```

Tests include:
- User signup/login/logout
- Task CRUD operations
- Authentication protection
- Input validation

## Development Notes

- Backend uses SQLite by default (tasks.db)
- JWT tokens expire after 20 minutes
- CORS is configured for localhost:3000
- All task endpoints require authentication

## Security Features

- Passwords hashed with bcrypt
- JWT token-based authentication
- Protected API routes
- CORS configuration
- Input validation on both frontend and backend

## Future Enhancements

- Task filtering and search
- Task categories/tags
- Due dates and reminders
- User profile management
- Dark mode theme

## Author

Created as part of Development Assessment
