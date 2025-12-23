# Task Management Frontend

React frontend for the Task Management System.

## Features

- User registration and login
- JWT-based authentication
- Task dashboard with grid layout
- Create, edit, delete tasks
- Task completion toggle
- Priority-based color coding
- Responsive design

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start
```

App runs at: http://localhost:3000

## Project Structure

```
src/
├── components/      # Reusable components
│   ├── TaskCard.js
│   └── TaskModal.js
├── context/         # State management
│   └── AuthContext.js
├── pages/           # Page components
│   ├── Login.js
│   ├── Signup.js
│   └── Dashboard.js
├── services/        # API integration
│   └── api.js
├── App.js
└── index.js
```

## Key Components

### Authentication
- **Login**: User login form
- **Signup**: User registration with validation
- **AuthContext**: Manages auth state and tokens

### Task Management
- **Dashboard**: Main task view with all user tasks
- **TaskCard**: Individual task display
- **TaskModal**: Create/edit task form

### Services
- **api.js**: Axios-based API service with interceptors

## API Integration

Backend URL: `http://localhost:8000`

All task endpoints require JWT token in Authorization header.

## Features in Detail

- **Protected Routes**: Redirect to login if not authenticated
- **Auto-logout**: Clears token on 401 errors
- **Task Sorting**: Incomplete first, then by priority
- **Form Validation**: Client-side validation before submit
- **Error Handling**: User-friendly error messages

## Tech Stack

- React 18
- React Router DOM
- Axios
- Context API
