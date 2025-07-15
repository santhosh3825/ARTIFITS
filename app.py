import streamlit as st                                                                              # type: ignore
import numpy as np                                                                                  # type: ignore
import subprocess                                                                                   # type: ignore
import os                                                                                           # type: ignore

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def personalized_diet_recommendation(age, gender, goal, preference="balanced", allergies=[]):
    base_diet = {
        "weight_loss": {
            "default": ["Leafy greens", "Lean protein (chicken, tofu)", "Whole grains", "Low-fat dairy"],
            "vegan": ["Tofu", "Chickpeas", "Quinoa", "Almond milk", "Vegetables"],
            "keto": ["Avocados", "Eggs", "Cheese", "Olive oil", "Leafy greens"]
        },
        "weight_gain": {
            "default": ["Nut butters", "Red meat", "Whole milk", "Rice", "Bananas"],
            "vegan": ["Nuts", "Lentils", "Avocados", "Oats", "Soy milk"],
            "keto": ["Fatty fish", "Cheese", "Coconut oil", "Nuts", "Eggs"]
        },
        "maintenance": {
            "default": ["Balanced plate (protein, carb, veg)", "Fruits", "Lean meat", "Whole grains"],
            "vegan": ["Legumes", "Grains", "Vegetables", "Fruits"],
            "keto": ["Moderate fats", "Non-starchy vegetables", "Fish", "Cheese"]
        }
    }

    age_category = "adult"
    if age < 13:
        age_category = "child"
    elif age < 18:
        age_category = "teen"
    elif age >= 60:
        age_category = "senior"

    age_nutrients = {
        "child": ["Calcium", "Iron-rich foods", "Milk", "Eggs"],
        "teen": ["Protein", "Zinc", "Dairy", "Iron"],
        "adult": ["Fiber", "Lean protein", "Omega-3"],
        "senior": ["Calcium", "Vitamin D", "Low-sodium", "High-fiber foods"]
    }

    gender_focus = {
        "male": ["More protein", "Iron", "Whole grains"],
        "female": ["Folic acid", "Iron", "Calcium"],
        "nonbinary": ["Balanced macros", "Plant-based proteins", "Vitamin D"]
    }

    plan = base_diet.get(goal, {}).get(preference, base_diet["maintenance"]["default"])
    plan += age_nutrients.get(age_category, [])
    plan += gender_focus.get(gender.lower(), [])

    clean_plan = [item for item in set(plan) if all(allergen.lower() not in item.lower() for allergen in allergies)]
    return list(sorted(clean_plan))

st.set_page_config(page_title="Smart Fitness & Diet Assistant", layout="centered")
st.title("💪 Smart Fitness & Diet Assistant")
st.header("📏 BMI & Diet Recommendation")
height = st.number_input("Enter your height (cm)", min_value=50.0, max_value=250.0, value=170.0)
weight = st.number_input("Enter your weight (kg)", min_value=20.0, max_value=250.0, value=70.0)
age = st.slider("Select your age", 5, 100, 25)
gender = st.selectbox("Select your gender", ["male", "female", "nonbinary"])
goal = st.selectbox("Your fitness goal", ["weight_loss", "weight_gain", "maintenance"])
preference = st.selectbox("Dietary preference", ["default", "vegan", "keto"])
allergies = st.text_input("Allergies (comma separated, optional)")
if st.button("Get Recommendation"):
    bmi = calculate_bmi(height, weight)
    bmi_status = bmi_category(bmi)
    allergy_list = [a.strip() for a in allergies.split(",") if a.strip()]
    st.subheader(f"📊 Your BMI: {bmi} ({bmi_status})")
    diet = personalized_diet_recommendation(age, gender, goal, preference, allergy_list)
    st.subheader("🍽 Recommended Foods")
    for item in diet:
        st.write(f"- {item}")
st.divider()
st.header("🏋️ Workout Tracker")
st.markdown("This feature opens a separate window to track your workout in real time.")

st.header("🏋️ Launch Specific Workout Counters")


workout_scripts = {
    "Sit-Up Counter": "situps.py",
    "Push-Up Counter": "pushup.py",
    "Squat Counter": "squat.py",
    "Lunge Counter": "lunges.py",
    "Bicep Curl Counter": "bicepcurl.py"
}

for label, filename in workout_scripts.items():
    if st.button(f"🚀 {label}"):
        script_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(script_path):
            try:
                subprocess.Popen(["python", script_path], shell=True)
                st.success(f"{label} launched in a separate window.")
            except Exception as e:
                st.error(f"❌ Failed to launch {label}: {e}")
        else:
            st.error(f"❌ Script file not found: {filename}")
