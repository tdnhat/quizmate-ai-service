from pydantic import BaseModel, Field
from typing import List, Optional, Union
from enum import Enum


class QuestionType(str, Enum):
    """Quiz question types."""
    SINGLE_CHOICE = "SingleChoice"
    TRUE_FALSE = "TrueFalse"


class DifficultyLevel(str, Enum):
    """Quiz difficulty levels."""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class Answer(BaseModel):
    """Model for quiz answer."""
    text: str = Field(..., description="The answer text")
    isCorrect: bool = Field(..., description="Whether the answer is correct")
    explanation: Optional[str] = Field(None, description="Explanation for this answer")


class Question(BaseModel):
    """Model for a quiz question."""
    text: str = Field(..., description="The question text")
    questionType: QuestionType = Field(..., description="Type of question")
    points: int = Field(1, ge=1, description="Points for this question")
    answers: List[Answer] = Field(..., min_items=2, max_items=6, description="Possible answers")
    explanation: Optional[str] = Field(None, description="Explanation for the question")
    imageUrl: Optional[str] = Field(None, description="URL to question image")


class QuizRequest(BaseModel):
    """Model for quiz generation request."""
    title: str = Field(..., min_length=3, description="Title for the quiz")
    difficulty: DifficultyLevel = Field(DifficultyLevel.INTERMEDIATE, description="Difficulty level")
    num_questions: int = Field(5, ge=1, le=20, description="Number of questions to generate")
    include_explanations: bool = Field(True, description="Whether to include explanations for answers")
    categoryId: str = Field(..., description="Category ID for the quiz")


class QuizResponse(BaseModel):
    """Model for quiz generation response."""
    title: str = Field(..., description="Title of the quiz")
    description: str = Field(..., description="Description of the quiz")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level of the quiz")
    categoryId: str = Field(..., description="Category ID of the quiz")
    timeMinutes: int = Field(..., ge=1, description="Time limit in minutes")
    questions: List[Question] = Field(..., description="List of quiz questions")
    passingScore: int = Field(60, description="Passing score percentage")
    tags: List[str] = Field(default_factory=list, description="Tags for the quiz")


# Legacy models for backward compatibility
class QuizQuestion(BaseModel):
    """Legacy model for a quiz question."""
    question: str = Field(..., description="The question text")
    options: List[str] = Field(..., min_items=2, max_items=5, description="List of possible answers")
    correct_answer: int = Field(..., ge=0, description="Index of the correct answer (0-based)")
    explanation: Optional[str] = Field(None, description="Explanation of why the answer is correct")
