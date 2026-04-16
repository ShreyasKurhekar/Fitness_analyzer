from pathlib import Path
from typing import Literal
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn

from health_calculator import HealthCalculator
from nutrition_api import NutritionAPI
from workout_advisor import WorkoutAdvisor


ROOT_DIR = Path(__file__).resolve().parent
ENV_PATHS = [ROOT_DIR / ".env", ROOT_DIR / "backend" / ".env"]
FRONTEND_FILE = ROOT_DIR / "frontend" / "index.html"

for env_path in ENV_PATHS:
    if env_path.exists():
        load_dotenv(env_path)
        break


app = FastAPI(title="Fitness Analyzer")

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
def index():
    if not FRONTEND_FILE.exists():
        raise HTTPException(status_code=404, detail="frontend/index.html not found")
    return FileResponse(FRONTEND_FILE)


@app.get("/health")
def health_check():
    return {"message": "Fitness Analyzer is running"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
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

# 🔑 ADD YOUR KEYS HERE
CONSUMER_KEY = "10b4bcdd0b0e4398b4c4e5aa2039e56f"
CONSUMER_SECRET = "f09b56a114ff42c395cb37fa2d742577"


def main():

    print("===== FITNESS ANALYZER =====\n")

    age = int(input("Enter age: "))
    weight = float(input("Enter weight (kg): "))
    height = float(input("Enter height (cm): "))
    goal = input("Goal (lose/gain/maintain): ").lower()
    food = input("Enter foods separated by commas (e.g. chicken, rice, egg): ")

    calc = HealthCalculator()

    bmi = calc.calculate_bmi(weight, height)
    category = calc.bmi_category(bmi)
    calories_needed = calc.calculate_calories(weight, height, age, goal)

    print("\n--- HEALTH DATA ---")
    print("BMI:", bmi, "|", category)
    print("Daily Calories Needed:", calories_needed)

    print("\n--- FOOD DATA ---")
    nutrition = NutritionAPI(CONSUMER_KEY, CONSUMER_SECRET)
    food_data = nutrition.get_multiple_food_data(food)

    for item in food_data:
        print(item)

    print("\n--- WORKOUT PLAN ---")
    workout = WorkoutAdvisor().get_workout(goal, age, bmi, category)

    for w in workout:
        print("-", w)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
