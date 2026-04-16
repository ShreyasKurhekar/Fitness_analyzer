class WorkoutAdvisor:
    def get_workout(self, goal, age, bmi, bmi_category):
        if goal == "lose":
            return self._build_weight_loss_plan(age, bmi, bmi_category)
        if goal == "gain":
            return self._build_muscle_gain_plan(age, bmi, bmi_category)
        return self._build_maintenance_plan(age, bmi, bmi_category)

    def get_diet_plan(self, goal, diet_type):
        normalized_type = diet_type.strip().lower()
        if normalized_type == "non veg":
            return self._build_non_veg_diet(goal)
        return self._build_veg_diet(goal)

    def _build_weight_loss_plan(self, age, bmi, bmi_category):
        cardio = "Brisk walking or light cycling for 30-40 min, 5 days/week"
        if bmi >= 30:
            cardio = "Low-impact cardio like incline walking or cycling for 35-45 min, 5 days/week"
        elif bmi < 25 and age <= 35:
            cardio = "Jogging, cycling, or rowing for 30-40 min, 4-5 days/week"

        finisher = "Beginner intervals: 30 sec fast + 90 sec easy for 10 rounds, 1-2 days/week"
        if age <= 35 and bmi < 30:
            finisher = "HIIT: 40 sec hard + 20 sec rest for 15-20 min, 2 days/week"

        strength = "Full-body strength training 2-3 days/week to protect muscle while losing fat"
        if bmi_category == "Obese":
            strength = "Chair squats, wall push-ups, and band rows 2-3 days/week for joint-friendly strength"

        mobility = "10 min mobility work after sessions plus 1 recovery walk on the weekend"
        return [cardio, strength, finisher, mobility]

    def _build_muscle_gain_plan(self, age, bmi, bmi_category):
        split = "Upper/lower strength split 4 days/week with progressive overload"
        if age >= 40:
            split = "Full-body strength training 3 days/week with an extra rest day for recovery"
        elif bmi_category == "Underweight":
            split = "Full-body compound lifts 3-4 days/week focused on form and steady weight increases"

        compounds = "Prioritize squats, presses, rows, deadlifts, and lunges for 3-4 sets each"
        accessory = "Add push-ups, core work, and resistance-band accessories 2-3 times/week"
        recovery = "Keep cardio light: 15-20 min walking or cycling 2 days/week to support recovery"
        return [split, compounds, accessory, recovery]

    def _build_maintenance_plan(self, age, bmi, bmi_category):
        base = "Balanced routine: 150 min moderate cardio plus 2 strength sessions each week"
        if bmi_category in {"Overweight", "Obese"}:
            base = "Moderate cardio 30 min, 4-5 days/week plus 2 low-impact strength sessions"
        elif bmi_category == "Underweight":
            base = "Light cardio 20-25 min, 3 days/week plus 3 strength sessions to build stability"

        strength = "Mix bodyweight and dumbbell training for full-body strength and posture"
        if age >= 45:
            strength = "Use moderate resistance, controlled reps, and extra warm-up time for joint safety"

        flexibility = "Yoga or stretching 2-3 days/week to improve mobility and recovery"
        lifestyle = "Aim for 7k-10k steps daily and keep one full rest day each week"
        return [base, strength, flexibility, lifestyle]

    def _build_veg_diet(self, goal):
        if goal == "lose":
            return [
                "Breakfast: Oats + chia seeds + seasonal fruit",
                "Lunch: 2 rotis + dal + mixed vegetable sabzi + salad",
                "Snack: Roasted chana or sprouts chaat",
                "Dinner: Paneer/tofu stir-fry with sauteed vegetables",
            ]
        if goal == "gain":
            return [
                "Breakfast: Peanut butter toast + banana + milk",
                "Lunch: Rice + rajma/chole + paneer + salad",
                "Snack: Dry fruits + banana smoothie",
                "Dinner: 3 rotis + soy/paneer bhurji + curd",
            ]
        return [
            "Breakfast: Idli/upma/poha with nuts",
            "Lunch: 2 rotis + dal + vegetables + curd",
            "Snack: Fruit + buttermilk",
            "Dinner: Khichdi or roti with paneer/tofu and salad",
        ]

    def _build_non_veg_diet(self, goal):
        if goal == "lose":
            return [
                "Breakfast: Boiled eggs + whole wheat toast + fruit",
                "Lunch: Grilled chicken/fish + brown rice + salad",
                "Snack: Greek yogurt or boiled eggs",
                "Dinner: Egg white omelette + sauteed vegetables",
            ]
        if goal == "gain":
            return [
                "Breakfast: 3-4 eggs + oats + milk",
                "Lunch: Chicken breast + rice + mixed vegetables",
                "Snack: Peanut butter sandwich + banana",
                "Dinner: Fish/chicken curry + 3 rotis + curd",
            ]
        return [
            "Breakfast: 2 eggs + vegetable sandwich",
            "Lunch: Chicken/fish + 2 rotis + salad",
            "Snack: Fruit + yogurt",
            "Dinner: Light chicken soup + sauteed vegetables + roti",
        ]
