"""
Student Name: Couger Jaramillo
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Survival Prognosis Predictor", layout="centered")

st.title("🏥 Clinical Prognosis Predictor")
st.markdown("""
Enter the patient's clinical parameters below to predict their survival category 
based on the trained Logistic Regression model.
""")

st.sidebar.header("Patient Data")

# Number input for Age
age = st.sidebar.number_input(
    "Age at Scan (years)",
    min_value=0,
    max_value=120,
    value=55,
    step=1
)

# Selection menus
gender = st.sidebar.selectbox("Gender", options=["Male", "Female"])
idh1 = st.sidebar.selectbox("IDH1 Status", options=["Wildtype", "Mutated"])
mgmt = st.sidebar.selectbox("MGMT Status", options=["Unmethylated", "Methylated"])
gtr = st.sidebar.selectbox("GTR > 90%", options=["Yes", "No"])

# Mapping inputs to the binary/numeric values used in your Capstone.ipynb
gender_val = 1 if gender == "Male" else 0
idh1_val = 1 if idh1 == "Mutated" else 0
mgmt_val = 1 if mgmt == "Methylated" else 0
gtr_val = 1 if gtr == "Yes" else 0

# Feature array in the exact order: [Gender, Age, IDH1, MGMT, GTR]
features = np.array([[gender_val, age, idh1_val, mgmt_val, gtr_val]])


#Model Loading
@st.cache_resource
def load_model():
    try:
        return joblib.load('trained_model.pkl')
    except:
        return None


model = load_model()

# Prediction function
if st.button("Predict Prognostic Class"):
    st.divider()

    if model is not None:
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]

        st.subheader("Results")

        # 2 classes
        if prediction == 0:
            st.success("The model predicts: **Class 0 (High Survival Probability)**")
        else:
            st.warning("The model predicts: **Class 1 (Lower Survival Probability)**")

        # Display Probabilities for transparency
        col1, col2 = st.columns(2)
        col1.metric("Class 0 Prob", f"{probabilities[0] * 100:.1f}%")
        col2.metric("Class 1 Prob", f"{probabilities[1] * 100:.1f}%")
    else:
        # just in case
        st.error("Model file 'trained_model.pkl' not found. Please ensure it is in the same folder as this app.")
        st.info("In your notebook, run: `joblib.dump(fit, 'trained_model.pkl')` to export it.")

    st.caption("Disclaimer: This tool is for research purposes only.")