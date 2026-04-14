from flask import Flask, request, jsonify
import pickle
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load model and categories
def get_resource_path(relative_path):
    # For Vercel, files are relative to the root
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), relative_path)

model_path = get_resource_path('best_salary_model.pkl')
categories_path = get_resource_path('categories.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

with open(categories_path, 'rb') as f:
    categories = pickle.load(f)

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        age = float(data['age'])
        gender = data['gender']
        education = data['education']
        job_title = data['job_title']
        years_exp = float(data['years_exp'])

        # Encoding
        le = LabelEncoder()
        
        le.fit(categories['Gender'])
        gender_encoded = le.transform([gender])[0]
        
        le.fit(categories['Education Level'])
        edu_encoded = le.transform([education])[0]
        
        le.fit(categories['Job Title'])
        job_encoded = le.transform([job_title])[0]
        
        features = np.array([[age, gender_encoded, edu_encoded, job_encoded, years_exp]])
        prediction = model.predict(features)[0]
        
        return jsonify({'salary': round(prediction, 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(categories)

# For Vercel
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return "API is running"

if __name__ == "__main__":
    app.run()
