# Stack Overflow Clone API

A FastAPI-based REST API that replicates core Stack Overflow functionality including user authentication, questions, answers, voting, and comments.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Questions & Answers**: CRUD operations for questions and answers
- **Voting System**: Upvote/downvote questions and answers
- **Comments**: Add comments to questions and answers
- **Tags**: Categorize questions with tags
- **Search**: Search questions by title and content
- **User Profiles**: User management and profiles

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT with Python-Jose
- **Password Hashing**: Passlib with bcrypt
- **Migrations**: Alembic
- **Testing**: Pytest

## Project Structure

```
faststack/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection and session
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── question.py
│   │   ├── answer.py
│   │   ├── comment.py
│   │   ├── vote.py
│   │   └── tag.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── question.py
│   │   ├── answer.py
│   │   ├── comment.py
│   │   └── auth.py
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── questions.py
│   │   │   ├── answers.py
│   │   │   ├── comments.py
│   │   │   └── tags.py
│   │   └── deps.py             # Dependencies (auth, etc.)
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── security.py         # JWT and password utilities
│   │   └── config.py           # Environment configuration
│   └── crud/                   # CRUD operations
│       ├── __init__.py
│       ├── user.py
│       ├── question.py
│       ├── answer.py
│       ├── comment.py
│       └── tag.py
├── alembic/                    # Database migrations
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
├── tests/                      # Test files
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_questions.py
│   └── test_answers.py
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd faststack
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secret key
   ```

5. **Set up PostgreSQL database**
   - Create a PostgreSQL database
   - Update the DATABASE_URL in your .env file

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users/{user_id}` - Get user by ID

### Questions
- `GET /api/v1/questions` - List questions (with pagination and filters)
- `POST /api/v1/questions` - Create a new question
- `GET /api/v1/questions/{question_id}` - Get question by ID
- `PUT /api/v1/questions/{question_id}` - Update question
- `DELETE /api/v1/questions/{question_id}` - Delete question
- `POST /api/v1/questions/{question_id}/vote` - Vote on question

### Answers
- `GET /api/v1/questions/{question_id}/answers` - Get answers for a question
- `POST /api/v1/questions/{question_id}/answers` - Create answer for a question
- `PUT /api/v1/answers/{answer_id}` - Update answer
- `DELETE /api/v1/answers/{answer_id}` - Delete answer
- `POST /api/v1/answers/{answer_id}/vote` - Vote on answer

### Comments
- `GET /api/v1/questions/{question_id}/comments` - Get comments for a question
- `POST /api/v1/questions/{question_id}/comments` - Add comment to question
- `GET /api/v1/answers/{answer_id}/comments` - Get comments for an answer
- `POST /api/v1/answers/{answer_id}/comments` - Add comment to answer

### Tags
- `GET /api/v1/tags` - List all tags
- `POST /api/v1/tags` - Create a new tag

## Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License. 