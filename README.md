# Task 19 - Multi-User Task Management API

## Overview

This project implements a secure multi-user Task Management API using FastAPI, SQLAlchemy, SQLite, JWT authentication, and Pydantic validation.

The API allows authenticated users to create, view, update, and delete their own tasks. User-specific authorization is implemented to prevent unauthorized access to another user's tasks and protect against Insecure Direct Object Reference (IDOR).

## Objectives

- Implement user registration and authentication
- Generate secure JWT access tokens
- Implement complete Task CRUD operations
- Associate every task with its owner
- Prevent users from accessing another user's tasks
- Validate request data using Pydantic
- Store application data using SQLAlchemy and SQLite
- Provide interactive API documentation
- Create automated API tests

## Technologies Used

- Python 3.14
- FastAPI
- SQLAlchemy
- SQLite
- JWT
- python-jose
- Passlib + bcrypt
- Pydantic
- pytest
- HTTPX
- Uvicorn

## Project Structure

```text
task19-multi-user-task-api/
¦
+-- app/
¦   +-- __init__.py
¦   +-- main.py
¦   +-- database.py
¦   +-- models.py
¦   +-- schemas.py
¦   +-- auth.py
¦   +-- dependencies.py
¦
+-- tests/
¦   +-- test_api.py
¦
+-- .env
+-- .gitignore
+-- pytest.ini
+-- requirements.txt
+-- README.md
Database Design

The application uses two related tables:

+-------------------+
|       Users       |
+-------------------+
| id (PK)           |
| username          |
| email             |
| hashed_password   |
+---------+---------+
          |
          | 1 : Many
          |
+---------v---------+
|       Tasks       |
+-------------------+
| id (PK)           |
| title             |
| description       |
| completed         |
| user_id (FK)      |
+-------------------+

Each user can own multiple tasks, while every task belongs to exactly one user.

Authentication Flow
User
  |
  v
Register
  |
  v
Login
  |
  v
JWT Access Token
  |
  v
Protected Task API
  |
  v
Current User

Passwords are hashed using bcrypt and are never stored as plain text.

JWT authentication is used to identify the currently authenticated user.

Authorization and IDOR Protection

The API validates task ownership on protected task operations.

For example, when retrieving a task:

Task ID + Current User ID
          |
          v
     Database Query
          |
     +----+----+
     |         |
   Match    No Match
     |         |
     v         v
  Allow      404

A user cannot access another user's task simply by changing the task_id.

The database query checks both:

Task.id == task_id
Task.user_id == current_user.id

This prevents IDOR vulnerabilities and enforces user-specific authorization.

API Endpoints
Authentication
Method    Endpoint    Description    Authentication
POST    /auth/register    Register a new user    No
POST    /auth/login    Login and receive JWT    No
Task Management
Method    Endpoint    Description    Authentication
GET    /tasks    Get current user's tasks    Yes
POST    /tasks    Create a task    Yes
GET    /tasks/{task_id}    Get user's task    Yes
PUT    /tasks/{task_id}    Update user's task    Yes
DELETE    /tasks/{task_id}    Delete user's task    Yes
Validation

Pydantic validation is used for incoming data.

Examples:

Username: 3-50 characters
Password: 6-72 characters
Task title: 1-100 characters
Email: validated using EmailStr
Task completion: Boolean value
Environment Variables

Create a .env file:

SECRET_KEY=your-secret-key

The .env file is excluded from Git using .gitignore.

Never commit real secrets or passwords to the repository.

Installation

Clone the repository and enter the project directory:

git clone https://github.com/Mahima2005-shetty/task19-multi-user-task-api.git
cd task19-multi-user-task-api

Create a virtual environment:

python -m venv venv

Activate it on Windows:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
Run the Application

Start the FastAPI server:

uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000
API Documentation

FastAPI automatically provides interactive Swagger documentation:

http://127.0.0.1:8000/docs

OpenAPI specification:

http://127.0.0.1:8000/openapi.json

Swagger can be used to register users, authenticate users, create tasks, update tasks, and test authorization.

Testing

The project includes automated tests using pytest.

Run:

pytest -v

Current test coverage includes:

User registration
User login
Unauthorized task access
Complete Task CRUD
IDOR protection

Current result:

5 passed
Security Features
JWT-based authentication
Bcrypt password hashing
Environment-based secret configuration
Protected task endpoints
User-specific authorization
IDOR protection
Input validation
Database-level user-task relationship
Sensitive .env file excluded from Git
Example Task Request
{
  "title": "Complete Task 19",
  "description": "Build and test the multi-user task management API"
}

Example response:

{
  "id": 1,
  "title": "Complete Task 19",
  "description": "Build and test the multi-user task management API",
  "completed": false,
  "user_id": 1
}Conclusion

Task 19 demonstrates a secure multi-user Task Management API that combines authentication, authorization, database operations, validation, CRUD functionality, and automated testing.

The project specifically addresses the security requirement that users must only be able to manage their own tasks.
