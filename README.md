# QuizMate AI Service

An AI-powered quiz generation service built with LangChain and FastAPI, using Google's Gemini model.

## Features

- Generate quizzes on various topics based on predefined categories
- Multiple difficulty levels (Beginner, Intermediate, Advanced)
- Configurable number of questions
- Single-choice and true/false question types
- Automatic point calculation based on question complexity
- Reasonable passing score calculation (60-70% of total points)
- Optional explanations for correct answers
- RESTful API with Swagger documentation

## Setup and Installation

### Prerequisites

- Python 3.10+
- Google AI API key

### Environment Setup

1. Clone the repository and navigate to the project directory
2. Create and activate a virtual environment (Python venv or conda)
3. Install dependencies with `pip install -r requirements.txt`
4. Create a `.env` file based on `.env.example` and add your Google API key
5. Start the development server with `uvicorn app.main:app --reload`

The API will be available at http://localhost:8000 with Swagger documentation at http://localhost:8000/docs

## API Overview

The service provides the following endpoints:

- **POST `/api/quiz`**: Generate a new quiz based on category, difficulty, and number of questions
- **GET `/api/quiz/categories`**: Get a list of available quiz categories
- **GET `/api/quiz/topics`**: Get a list of topic names (derived from categories)

Detailed API documentation is available in the Swagger UI when the service is running.

## Integration with .NET Backend

To integrate this service with a .NET backend:

1. Configure the service URL in your .NET application
2. Create an HTTP client to communicate with the API
3. Register the client in your dependency injection container
4. Use the client in your controllers to request quizzes

Example configuration and implementation details can be found in the Swagger documentation.

## License

[MIT License](LICENSE)
