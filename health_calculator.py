class HealthCalculator:

    def calculate_bmi(self, weight, height):
        height_m = height / 100
        return round(weight / (height_m ** 2), 2)

    def bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def calculate_calories(self, weight, height, age, goal):
        bmr = 10 * weight + 6.25 * height - 5 * age + 5

        if goal == "lose":
            return int(bmr - 500)
        elif goal == "gain":
            return int(bmr + 500)
        return int(bmr)