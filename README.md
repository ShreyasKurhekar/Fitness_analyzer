# Fitness Analyzer Web App

This project converts the original Python CLI fitness tracker into a full-stack web app using FastAPI, Tailwind CSS, and Vanilla JavaScript.
The root [main.py](/c:/Users/shrey/OneDrive/Desktop/College/4th%20Sem/PL%20-Lab/fitness_tracker/main.py) now acts as the single local entry point and serves the web interface directly.

## Project Structure

```text
fitness_tracker/
|-- backend/
|   |-- .env
|   |-- health_calculator.py
|   |-- main.py
|   |-- nutrition_api.py
|   `-- workout_advisor.py
|-- frontend/
|   `-- index.html
|-- requirements.txt
`-- README.md
```

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Add API Keys

Update `backend/.env` or create a root `.env` with your FatSecret API credentials:

```env
CONSUMER_KEY=your_fatsecret_key
CONSUMER_SECRET=your_fatsecret_secret
```

## Run the App

Start the FastAPI server from the project root:

```bash
uvicorn main:app --reload
```

The app will be available at `http://127.0.0.1:8000`.

## Open the Frontend

Open `http://127.0.0.1:8000` in your browser after the server is running.

## API Endpoint

`POST /analyze`

Request body:

```json
{
  "age": 21,
  "weight": 68,
  "height": 172,
  "goal": "maintain",
  "food": "chicken"
}
```

Response body:

```json
{
  "bmi": 22.99,
  "bmi_category": "Normal",
  "daily_calories": 1660,
  "food_results": [
    "Chicken Breast - 165 kcal"
  ],
  "workout": [
    "Yoga",
    "Walking",
    "Stretching"
  ]
}
```
