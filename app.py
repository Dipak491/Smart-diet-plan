from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def calculate_bmi(weight, height):
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return round(bmi, 2), category


# ----------------- Diet Logic -----------------


def diet_plan(bmi, diet_type):
    if bmi < 18.5:
        return {
            "goal": "Weight Gain",
            "diet": ["Milk", "Banana", "Rice", "Paneer" if diet_type == 'veg' else "Eggs"],
            "protein": "High",
            "carbs": "High",
            "fats": "Medium"
        }
    elif bmi < 25:
        return {
            "goal": "Maintain Fitness",
            "diet": ["Vegetables", "Fruits", "Dal" if diet_type == 'veg' else "Chicken"],
            "protein": "Medium",
            "carbs": "Medium",
            "fats": "Low"
        }
    else:
        return {
            "goal": "Weight Loss",
            "diet": ["Salad", "Soup", "Oats"],
            "protein": "High",
            "carbs": "Low",
            "fats": "Low"
        }


# ----------------- API -----------------


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    bmi, category = calculate_bmi(float(data['weight']), float(data['height']))
    plan = diet_plan(bmi, data['dietType'])

    response = {
        "bmi": bmi,
        "category": category,
        "dietPlan": plan,
        "water": f"{float(data['weight']) * 0.033:.1f} Liters/day",
        "exercise": "Walking, Yoga" if bmi < 25 else "Cardio, HIIT",
        "motivation": "Stay consistent! Small progress is still progress 💪"
    }
    return jsonify(response)


# ----------------- Workout Database -----------------

WORKOUTS = {
    "weight_loss": {
        "gym": [
            {"exercise": "Treadmill", "sets": 1, "reps": "20 min"},
            {"exercise": "Cycling", "sets": 1, "reps": "15 min"},
            {"exercise": "Jump Squats", "sets": 3, "reps": 15},
            {"exercise": "Plank", "sets": 3, "reps": "30 sec"}
        ],
        "home": [
            {"exercise": "Jumping Jacks", "sets": 3, "reps": 30},
            {"exercise": "High Knees", "sets": 3, "reps": 20},
            {"exercise": "Mountain Climbers", "sets": 3, "reps": 15}
        ]
    },

    "weight_gain": {
        "gym": [
            {"exercise": "Bench Press", "sets": 4, "reps": 8},
            {"exercise": "Squats", "sets": 4, "reps": 8},
            {"exercise": "Deadlift", "sets": 4, "reps": 6},
            {"exercise": "Shoulder Press", "sets": 3, "reps": 10}
        ],
        "home": [
            {"exercise": "Push-ups", "sets": 4, "reps": 15},
            {"exercise": "Chair Squats", "sets": 4, "reps": 20},
            {"exercise": "Resistance Band Rows", "sets": 3, "reps": 15}
        ]
    },

    "maintenance": {
        "gym": [
            {"exercise": "Lat Pulldown", "sets": 3, "reps": 10},
            {"exercise": "Lunges", "sets": 3, "reps": 12},
            {"exercise": "Leg Press", "sets": 3, "reps": 10}
        ],
        "home": [
            {"exercise": "Bodyweight Squats", "sets": 3, "reps": 15},
            {"exercise": "Plank", "sets": 3, "reps": "45 sec"}
        ]
    }
}

@app.route('/workout', methods=['POST'])
def workout():
    data = request.json
    bmi = data['bmi']
    place = data['place']  # gym / home

    if bmi < 18.5:
        goal = "weight_gain"
    elif bmi < 25:
        goal = "maintenance"
    else:
        goal = "weight_loss"

    return jsonify({
        "goal": goal.replace("_", " ").title(),
        "workout": WORKOUTS[goal][place]
    })


if __name__ == '__main__':
    app.run(debug=True)