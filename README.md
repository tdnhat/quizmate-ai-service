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

- Python 3.10+ (for local development)
- Google AI API key
- Docker and Docker Compose (optional, for containerized deployment)
- Conda package manager (recommended)

### Environment Setup

#### Local Development

1. Clone the repository and navigate to the project directory
2. Create and activate a conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate quizmate
   ```
3. Create a `.env` file based on `.env.example` and add your Google API key
4. Start the development server with `uvicorn app.main:app --reload`

#### Docker Deployment

1. Clone the repository and navigate to the project directory
2. Create a `.env` file based on `.env.example` and add your Google API key
3. Build and start the container:
   ```bash
   docker-compose up -d
   ```
4. To stop the service:
   ```bash
   docker-compose down
   ```

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

## Deployment Options

### Docker (Recommended)

The simplest way to deploy the service is using Docker:

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

The Docker image uses Conda exclusively for package management, providing a consistent environment for development and production without requiring pip.

### Manual Deployment

For production deployment without Docker:

1. Set up a Python environment using conda and the provided environment.yml
2. Configure a production ASGI server like Gunicorn
3. Set up a reverse proxy (Nginx or similar)
4. Configure environment variables for production settings

## License

[MIT License](LICENSE)
