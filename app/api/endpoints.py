import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict

from app.models.quiz import QuizQuestion, QuizRequest, QuizResponse, DifficultyLevel, QuestionType
from app.services.quiz_generator import quiz_generator

# Initialize logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Category mapping
CATEGORIES = {
    "programming": "Programming",
    "computer_science": "Computer Science",
    "web_dev": "Web Development",
    "data_science": "Data Science",
    "devops": "DevOps",
    "cloud": "Cloud Computing",
    "security": "Cybersecurity",
    "databases": "Databases",
    "networking": "Networking",
    "mobile_dev": "Mobile Development"
}


@router.post("/quiz", response_model=QuizResponse, 
             summary="Generate a new quiz",
             description="Generate a quiz with custom topics based on category")
async def generate_quiz(request: QuizRequest):
    """
    Generate a quiz based on the request parameters.
    
    - **title**: Title for the quiz
    - **difficulty**: Difficulty level (Beginner, Intermediate, Advanced)
    - **num_questions**: Number of questions to generate (default: 5)
    - **include_explanations**: Whether to include explanations for answers (default: true)
    - **categoryId**: Category ID for the quiz (determines the topic)
    """
    try:
        # Get topic from category ID
        category_name = CATEGORIES.get(request.categoryId)
        if not category_name:
            raise HTTPException(status_code=400, detail=f"Invalid category ID: {request.categoryId}")
            
        logger.info(f"Generating quiz for category: {category_name}, difficulty: {request.difficulty}")
        
        # Generate quiz using LangChain service
        quiz = await quiz_generator.generate_quiz(
            topic=category_name,
            num_questions=request.num_questions,
            difficulty=request.difficulty,
            include_explanations=request.include_explanations,
            question_type=QuestionType.SINGLE_CHOICE,  # Default to SingleChoice
            title=request.title,
            description=f"A {request.difficulty.value} level quiz about {category_name}",
            category_id=request.categoryId,
            time_minutes=10  # Default time limit
        )
        
        return quiz
        
    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")


@router.get("/quiz/topics",
            summary="Get suggested quiz topics",
            description="Returns a list of suggested topics for quiz generation")
async def get_quiz_topics():
    """Get suggested quiz topics."""
    return {
        "topics": list(CATEGORIES.values())
    }


@router.get("/quiz/categories",
            summary="Get available quiz categories",
            description="Returns a list of available categories for quizzes")
async def get_quiz_categories():
    """Get quiz categories."""
    return {
        "categories": [
            {"id": id, "name": name} for id, name in CATEGORIES.items()
        ]
    }
