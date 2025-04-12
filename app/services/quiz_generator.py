import logging
from typing import List, Dict, Any, Optional
import json
import re
import math

# Replace OpenAI with Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from app.core.config import settings
from app.models.quiz import Question, Answer, QuestionType, DifficultyLevel, QuizResponse, QuizRequest

# Initialize logger
logger = logging.getLogger(__name__)


class QuizGeneratorService:
    """Service for generating quizzes using LangChain."""

    def __init__(self):
        """Initialize the quiz generator service."""
        self.llm = ChatGoogleGenerativeAI(
            temperature=0.2,
            model="gemini-2.0-flash-001",  # Using Gemini model
            google_api_key=settings.GOOGLE_API_KEY,
        )
        
        # Define prompt template
        self.prompt_template = ChatPromptTemplate.from_template(
            """
            You are an expert educational quiz maker. Create a quiz on the topic of {topic} with {num_questions} questions.
            The difficulty level should be {difficulty}.
            The question type should be {question_type}.
            
            IMPORTANT: You must return a valid JSON object with the following structure:
            
            ```json
            {{
              "title": "Quiz title here",
              "description": "Quiz description here",
              "questions": [
                {{
                  "text": "Question text",
                  "questionType": "{question_type}",
                  "points": 1,
                  "answers": [
                    {{ "text": "Answer option 1", "isCorrect": true, "explanation": "Why this is correct" }},
                    {{ "text": "Answer option 2", "isCorrect": false, "explanation": null }},
                    {{ "text": "Answer option 3", "isCorrect": false, "explanation": null }},
                    {{ "text": "Answer option 4", "isCorrect": false, "explanation": null }}
                  ],
                  "explanation": "Overall explanation for the question"
                }}
                // more questions...
              ]
            }}
            ```
            
            For "SingleChoice" questions, make exactly one answer correct.
            For "TrueFalse" questions, provide exactly two options: "True" and "False".
            
            Assign different point values to questions based on their difficulty. For example:
            - Simple questions: 1 point
            - Medium difficulty questions: 2 points
            - Challenging questions: 3 points
            
            The questions should be diverse and cover different aspects of the topic.
            Generate challenging but fair questions appropriate for the {difficulty} difficulty level.
            
            DO NOT include any additional text, only return the JSON object.
            """
        )
        
        # Create the LLMChain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    async def generate_quiz(
        self, 
        topic: str, 
        num_questions: int, 
        difficulty: DifficultyLevel,
        include_explanations: bool,
        question_type: QuestionType = QuestionType.SINGLE_CHOICE,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category_id: Optional[str] = None,
        time_minutes: int = 10
    ) -> QuizResponse:
        """
        Generate a quiz on a given topic.
        
        Args:
            topic: The topic for the quiz
            num_questions: Number of questions to generate
            difficulty: Difficulty level
            include_explanations: Whether to include explanations
            question_type: Type of questions to generate
            title: Title for the quiz (generated if not provided)
            description: Description for the quiz (generated if not provided)
            category_id: Category ID for the quiz
            time_minutes: Time limit in minutes
            
        Returns:
            QuizResponse object with quiz data
        """
        try:
            # Generate quiz using LangChain
            response = await self.chain.arun(
                topic=topic,
                num_questions=num_questions,
                difficulty=difficulty.value,
                question_type=question_type.value
            )
            
            logger.debug(f"Raw LLM response: {response}")
            
            # Extract JSON from response
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            
            if json_match:
                # Extract JSON content from between ```json ``` markers
                json_str = json_match.group(1)
                logger.debug(f"Extracted JSON: {json_str}")
            else:
                # Attempt to use the entire response
                json_str = response
            
            # Remove any leading/trailing whitespace and non-JSON text
            json_str = json_str.strip()
            
            # Try to find JSON object in the response if it's not properly formatted
            if not (json_str.startswith('{') and json_str.endswith('}')):
                obj_match = re.search(r'\{\s*".*"\s*:\s*.*\}', json_str, re.DOTALL)
                if obj_match:
                    json_str = obj_match.group(0)
            
            try:
                # Parse JSON
                data = json.loads(json_str)
                
                # Get generated title and description if not provided
                if not title and "title" in data:
                    title = data["title"]
                elif not title:
                    title = f"Quiz on {topic}"
                    
                if not description and "description" in data:
                    description = data["description"]
                elif not description:
                    description = f"A {difficulty.value.lower()} level quiz about {topic}"
                
                # Process questions
                questions = []
                total_points = 0
                
                for q in data.get("questions", []):
                    # Get or default the points value
                    points = q.get("points", 1)
                    total_points += points
                    
                    question = Question(
                        text=q["text"],
                        questionType=q.get("questionType", question_type.value),
                        points=points,
                        answers=[
                            Answer(
                                text=a["text"],
                                isCorrect=a["isCorrect"],
                                explanation=a.get("explanation") if include_explanations else None
                            ) for a in q["answers"]
                        ],
                        explanation=q.get("explanation") if include_explanations else None,
                        imageUrl=q.get("imageUrl")
                    )
                    questions.append(question)
                
                # Calculate a reasonable passing score (at most 70% of total points)
                passing_score = int(math.ceil(0.6 * total_points))  # Minimum 60%
                passing_score = min(passing_score, int(0.7 * total_points))  # Maximum 70% 
                
                # Create quiz response
                quiz = QuizResponse(
                    title=title,
                    description=description,
                    difficulty=difficulty,
                    categoryId=category_id,
                    timeMinutes=time_minutes,
                    questions=questions,
                    passingScore=passing_score,
                    tags=[topic]  # Use topic as default tag
                )
                
                return quiz
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from LLM response: {e}")
                logger.debug(f"Attempted to parse: {json_str}")
                raise ValueError("Failed to parse quiz data from LLM response")
        
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            raise
    
    
# Create a singleton instance
quiz_generator = QuizGeneratorService()
