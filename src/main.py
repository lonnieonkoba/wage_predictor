import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load the data
data = pd.read_csv('data/Salaries.csv')

# Split the data into features and target
X = data[['YearsExperience', 'Degree']]
y = data['Salary']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression object
model = LinearRegression()

# Train the model on the training data
model.fit(X_train, y_train)

# Use the trained model to make predictions on the testing data
predictions = model.predict(X_test)

# Create a Streamlit app
st.title('Wage Salary Predictor')
st.write('This app predicts salaries for people based on their years of experience and degree.')

# Get user input for years of experience and degree
years_experience = st.number_input('Years of experience:')
degree = st.selectbox('Degree:', ['Bachelors', 'Masters', 'PhD'])

# Use the trained model to make a prediction for the user's input
prediction = model.predict([[years_experience, degree.lower()]])

# Display the user's input and the predicted salary
st.write(f'Based on {years_experience} years of experience and a {degree}, the predicted salary is ${prediction[0]:.2f}.')
