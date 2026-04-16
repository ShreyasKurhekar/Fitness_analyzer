from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os

from backend.health_calculator import HealthCalculator
from backend.nutrition_api import NutritionAPI
from backend.workout_advisor import WorkoutAdvisor


load_dotenv(Path(__file__).with_name(".env"))

app = FastAPI(title="Fitness Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    age: int = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    goal: Literal["lose", "gain", "maintain"]
    food: str = Field(..., min_length=1, description="Comma-separated food items")


class AnalyzeResponse(BaseModel):
    bmi: float
    bmi_category: str
    daily_calories: int
    food_results: list[str]
    workout: list[str]


@app.get("/")
def health_check():
    return {"message": "Fitness Analyzer API is running"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_fitness(payload: AnalyzeRequest):
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")

    calculator = HealthCalculator()
    bmi = calculator.calculate_bmi(payload.weight, payload.height)
    bmi_category = calculator.bmi_category(bmi)
    daily_calories = calculator.calculate_calories(
        payload.weight,
        payload.height,
        payload.age,
        payload.goal,
    )

    nutrition = NutritionAPI(consumer_key, consumer_secret)
    food_results = nutrition.get_multiple_food_data(payload.food.strip())
    workout = WorkoutAdvisor().get_workout(
        payload.goal,
        payload.age,
        bmi,
        bmi_category,
    )

    return AnalyzeResponse(
        bmi=bmi,
        bmi_category=bmi_category,
        daily_calories=daily_calories,
        food_results=food_results,
        workout=workout,
    )
