# ⚡ SmartWatt Pakistan

SmartWatt Pakistan is a Machine Learning-powered web application designed to predict electricity consumption/cost based on household-related inputs.

The project demonstrates a complete Machine Learning workflow, from model training and evaluation to API development and deployment.

## 🚀 Live Demo

https://app-peach-phi-78.vercel.app/

## 📌 Project Overview

The goal of this project is to use Machine Learning to generate electricity-related predictions based on input features provided by the user.

## 🧠 Machine Learning

* **Algorithm:** Linear Regression
* **Data Preprocessing:** Feature scaling
* **Model Evaluation:** MSE and R² Score
* **Model Serialization:** Joblib / Pickle

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib
* Flask
* HTML/CSS
* Vercel

## 🔄 Machine Learning Workflow

```text
Dataset
   ↓
Data Preprocessing
   ↓
Feature Scaling
   ↓
Train/Test Split
   ↓
Linear Regression
   ↓
Model Evaluation
   ↓
Save Model
   ↓
Flask API
   ↓
Web Application
   ↓
Vercel Deployment
```

## 📂 Project Structure

```text
SmartWatt-Pakistan/
│
├── api/
│   └── index.py
│
├── static/
│
├── templates/
│
├── linear_regression_model.pkl
├── scaler.pkl
├── requirements.txt
├── .gitignore
└── README.md
```

## 📊 Model Evaluation

The model was evaluated using:

### Mean Squared Error (MSE)

MSE measures the average squared difference between actual and predicted values.

### R² Score

R² Score measures how well the model explains the variation in the target variable.

## 🌐 Deployment

The Flask-based application is deployed using **Vercel**, making the Machine Learning prediction system accessible through a web interface.

## 🎯 Learning Outcomes

Through this project, I practiced:

* Machine Learning model development
* Data preprocessing
* Model evaluation
* Saving and loading ML models
* Flask API development
* Git and GitHub
* Cloud deployment
* Connecting an ML model with a web application

## 🔮 Future Improvements

* Experiment with additional regression algorithms
* Improve model performance through hyperparameter tuning
* Add more relevant features
* Improve the user interface
* Add more detailed prediction insights

## 👨‍💻 Project

Built as part of my journey in **Machine Learning, AI, and Python development**.
