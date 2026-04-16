import requests
from requests_oauthlib import OAuth1


class NutritionAPI:
    FALLBACK_DATASET = {
        "apple": {"name": "Apple", "calories": 52},
        "banana": {"name": "Banana", "calories": 89},
        "bread": {"name": "Bread", "calories": 265},
        "chicken": {"name": "Chicken Breast", "calories": 165},
        "egg": {"name": "Egg", "calories": 155},
        "milk": {"name": "Milk", "calories": 42},
        "oats": {"name": "Oats", "calories": 389},
        "orange": {"name": "Orange", "calories": 47},
        "paneer": {"name": "Paneer", "calories": 265},
        "rice": {"name": "Rice", "calories": 130},
    }

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.url = "https://platform.fatsecret.com/rest/server.api"

    def _dataset_results(self, query):
        query_text = query.strip().lower()
        matches = []

        for keyword, item in self.FALLBACK_DATASET.items():
            if keyword in query_text or query_text in keyword:
                matches.append(f"{item['name']} - {item['calories']} kcal")

        if matches:
            return matches[:3]

        return [
            f"{item['name']} - {item['calories']} kcal"
            for item in list(self.FALLBACK_DATASET.values())[:3]
        ]

    def _extract_calories(self, food_item, detail_data):
        compact_description = food_item.get("food_description", "")
        if compact_description:
            parts = [part.strip() for part in compact_description.split("|")]
            for part in parts:
                if "kcal" in part.lower():
                    return part.replace("Calories:", "").replace("calories:", "").strip()

        try:
            serving = detail_data["food"]["servings"]["serving"]
            if isinstance(serving, list):
                serving = serving[0]

            calories = serving.get("calories")
            if calories:
                return f"{calories} kcal"
        except Exception:
            pass

        return "N/A kcal"

    def get_food_data(self, query):
        if not self.key or not self.secret:
            return self._dataset_results(query)

        auth = OAuth1(self.key, self.secret)

        params = {
            "method": "foods.search",
            "search_expression": query,
            "format": "json",
        }

        try:
            response = requests.get(self.url, params=params, auth=auth, timeout=15)
        except requests.RequestException:
            return self._dataset_results(query)

        if response.status_code != 200:
            return self._dataset_results(query)

        try:
            data = response.json()
        except ValueError:
            return self._dataset_results(query)
        foods = data.get("foods", {}).get("food", [])

        if isinstance(foods, dict):
            foods = [foods]

        if not foods:
            return self._dataset_results(query)

        results = []

        for item in foods[:3]:
            food_id = item["food_id"]
            name = item["food_name"]

            detail_params = {
                "method": "food.get",
                "food_id": food_id,
                "format": "json",
            }

            try:
                detail_res = requests.get(
                    self.url,
                    params=detail_params,
                    auth=auth,
                    timeout=15,
                )
                detail_data = detail_res.json() if detail_res.status_code == 200 else {}
            except (requests.RequestException, ValueError):
                detail_data = {}
            calories = self._extract_calories(item, detail_data)
            results.append(f"{name} - {calories}")

        return results or self._dataset_results(query)

    def get_multiple_food_data(self, query_text):
        combined_results = []
        seen_items = set()

        foods = [item.strip() for item in query_text.split(",") if item.strip()]

        for food in foods:
            for result in self.get_food_data(food):
                if result not in seen_items:
                    seen_items.add(result)
                    combined_results.append(result)

        return combined_results or self._dataset_results(query_text)
