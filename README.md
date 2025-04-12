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

1. Clone the repository:
```bash
git clone https://github.com/yourusername/quizmate-ai-service.git
cd quizmate-ai-service
```

2. Create a virtual environment:
```bash
python -m venv venv
# or with conda
conda create -n quizmate-ai python=3.10
conda activate quizmate-ai
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

6. Edit the `.env` file to add your Google API key.

### Running the Service

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000
Swagger documentation is available at http://localhost:8000/docs

## API Models

### Quiz Generation Request

```json
{
  "title": "Python Basics",
  "difficulty": "Intermediate",
  "num_questions": 5,
  "include_explanations": true,
  "categoryId": "programming"
}
```

- `title`: Title for the quiz (min 3 characters)
- `difficulty`: "Beginner", "Intermediate", or "Advanced"
- `num_questions`: Number of questions (1-20)
- `include_explanations`: Whether to include explanations for answers
- `categoryId`: ID of the category (determines the topic)

### Quiz Response

```json
{
  "title": "Python Basics",
  "description": "An Intermediate level quiz about Programming",
  "difficulty": "Intermediate",
  "categoryId": "programming",
  "timeMinutes": 10,
  "questions": [
    {
      "text": "What does the 'self' parameter in Python class methods represent?",
      "questionType": "SingleChoice",
      "points": 2,
      "answers": [
        {
          "text": "The instance of the class",
          "isCorrect": true,
          "explanation": "In Python, 'self' refers to the instance of the class and is used to access variables and methods of the class."
        },
        {
          "text": "The class itself",
          "isCorrect": false
        },
        {
          "text": "The module containing the class",
          "isCorrect": false
        },
        {
          "text": "A required keyword in Python",
          "isCorrect": false
        }
      ],
      "explanation": "Understanding 'self' is crucial for object-oriented programming in Python."
    }
  ],
  "passingScore": 7,
  "tags": ["Programming"]
}
```

## API Endpoints

### Generate a Quiz

**Endpoint:** POST `/api/quiz`

Generates a new quiz based on the provided parameters.

### Get Categories

**Endpoint:** GET `/api/quiz/categories`

Returns a list of available quiz categories:

```json
{
  "categories": [
    {"id": "programming", "name": "Programming"},
    {"id": "computer_science", "name": "Computer Science"},
    {"id": "web_dev", "name": "Web Development"},
    // more categories...
  ]
}
```

### Get Topics

**Endpoint:** GET `/api/quiz/topics`

Returns a list of topic names (same as category names):

```json
{
  "topics": [
    "Programming", 
    "Computer Science", 
    "Web Development",
    // more topics...
  ]
}
```

## Integration with .NET Backend

To integrate this service with a .NET backend:

1. Add the service URL to your .NET application's configuration:
```json
"QuizService": {
  "BaseUrl": "http://localhost:8000",
  "TimeoutSeconds": 30
}
```

2. Create a REST client in your .NET application:
```csharp
// Example HTTP client class
public class QuizServiceClient
{
    private readonly HttpClient _httpClient;
    
    public QuizServiceClient(HttpClient httpClient, IOptions<QuizServiceOptions> options)
    {
        _httpClient = httpClient;
        _httpClient.BaseAddress = new Uri(options.Value.BaseUrl);
    }
    
    public async Task<QuizResponse> GenerateQuizAsync(QuizRequest request)
    {
        var response = await _httpClient.PostAsJsonAsync("/api/quiz", request);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<QuizResponse>();
    }
    
    public async Task<CategoriesResponse> GetCategoriesAsync()
    {
        return await _httpClient.GetFromJsonAsync<CategoriesResponse>("/api/quiz/categories");
    }
}
```

3. Register the client in your DI container:
```csharp
services.AddHttpClient<QuizServiceClient>();
```

4. Use the client in your API controller:
```csharp
[ApiController]
[Route("api/quizzes")]
public class QuizzesController : ControllerBase
{
    private readonly QuizServiceClient _quizService;
    
    public QuizzesController(QuizServiceClient quizService)
    {
        _quizService = quizService;
    }
    
    [HttpPost]
    public async Task<IActionResult> GenerateQuiz(QuizRequest request)
    {
        var quiz = await _quizService.GenerateQuizAsync(request);
        return Ok(quiz);
    }
}
```

## License

[MIT License](LICENSE)
