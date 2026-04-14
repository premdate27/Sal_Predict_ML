import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Set page config
st.set_page_config(page_title="Salary Prediction App", page_icon="💸", layout="centered")

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .prediction-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 20px;
    }
    .salary-text {
        font-size: 2.5em;
        color: #28a745;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the saved model
@st.cache_resource
def load_model():
    with open('best_salary_model.pkl', 'rb') as f:
        return pickle.load(f)

# Load categories for encoding
@st.cache_resource
def load_categories():
    with open('categories.pkl', 'rb') as f:
        return pickle.load(f)

model = load_model()
categories = load_categories()

st.title("💸 Salary Prediction App")
st.write("Predict your potential salary based on your experience, education, and job role.")

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Enter your Age", min_value=18.0, max_value=100.0, value=25.0, step=1.0)
        gender = st.selectbox("Select your Gender", options=categories['Gender'])
        education = st.selectbox("Education Level", options=categories['Education Level'])
        
    with col2:
        years_exp = st.number_input("Years of Experience", min_value=0.0, max_value=50.0, value=2.0, step=0.5)
        job_title = st.selectbox("Select your Job Title", options=categories['Job Title'])

# Prediction logic
if st.button("Predict Salary"):
    try:
        # Prepare inputs
        # Note: The model expects columns: ['Age', 'Gender', 'Education Level', 'Job Title', 'Years of Experience']
        
        # We must encode categorical variables exactly as during training
        # Since we have the sorted unique values, fitting a new LabelEncoder works
        le = LabelEncoder()
        
        le.fit(categories['Gender'])
        gender_encoded = le.transform([gender])[0]
        
        le.fit(categories['Education Level'])
        edu_encoded = le.transform([education])[0]
        
        le.fit(categories['Job Title'])
        job_encoded = le.transform([job_title])[0]
        
        # Combine into features array
        features = np.array([[age, gender_encoded, edu_encoded, job_encoded, years_exp]])
        
        # Predict
        prediction = model.predict(features)
        
        # Display Result
        st.markdown(f"""
            <div class="prediction-card">
                <h3>Estimated Annual Salary</h3>
                <div class="salary-text">${prediction[0]:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error during prediction: {e}")

st.divider()
st.info("💡 Note: The prediction is based on a Random Forest model trained on historical salary data.")
