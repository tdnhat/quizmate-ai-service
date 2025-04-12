# QuizMate AI Service

An AI-powered quiz generation service built with LangChain and FastAPI.

## Features

- Generate custom quizzes on various topics
- Adjustable difficulty levels (easy, medium, hard)
- Configurable number of questions
- Optional explanations for correct answers
- Built with LangChain for LLM integration
- RESTful API with FastAPI

## Setup and Installation

### Prerequisites

- Python 3.10+
- OpenAI API key (or other LLM provider key)

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/quizmate-ai-service.git
cd quizmate-ai-service
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

6. Edit the `.env` file to add your API keys and configuration.

### Running the Service

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Usage

### Generate a Quiz

**Endpoint:** POST `/api/quiz`

**Request Body:**
```json
{
  "topic": "Python Programming",
  "difficulty": "medium",
  "num_questions": 5,
  "include_explanations": true
}
```

**Response:**
```json
{
  "topic": "Python Programming",
  "difficulty": "medium",
  "questions": [
    {
      "question": "What is the output of print(1 + '1') in Python?",
      "options": [
        "2", 
        "11", 
        "TypeError", 
        "1"
      ],
      "correct_answer": 2,
      "explanation": "Python cannot add an integer and a string, resulting in a TypeError."
    },
    // More questions...
  ]
}
```

### Get Suggested Topics

**Endpoint:** GET `/api/quiz/topics`

**Response:**
```json
{
  "topics": [
    "Python Programming",
    "Data Structures",
    "Algorithms",
    // More topics...
  ]
}
```

## Integration with .NET Backend

To integrate this service with a .NET backend:

1. Add the service URL to your .NET application's configuration
2. Create a REST client in your .NET application to call the API
3. Implement proper error handling and retries
4. Consider adding a caching layer for performance

## License

[MIT License](LICENSE)
