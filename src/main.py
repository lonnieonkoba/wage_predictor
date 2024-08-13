import streamlit as st
import pickle
import numpy as np
import os
import socket
import pandas as pd


# Function to load the model and other data
def load_model():
    with open("saved_steps.pkl", "rb") as file:
        data = pickle.load(file)
    return data


# Function to initialize the CSV file
def init_csv():
    if not os.path.exists("user_data.csv"):
        df = pd.DataFrame(
            columns=[
                "IP",
                "Country",
                "Job Type",
                "Education",
                "Experience",
                "Predicted Salary",
            ]
        )
        df.to_csv("user_data.csv", index=False)


# Function to log user data to the CSV file
def log_user_data(ip, country, job_type, education, experience, salary):
    df = pd.DataFrame(
        [[ip, country, job_type, education, experience, salary]],
        columns=[
            "IP",
            "Country",
            "Job Type",
            "Education",
            "Experience",
            "Predicted Salary",
        ],
    )
    df.to_csv("user_data.csv", mode="a", header=False, index=False)


# Load model and label encoders
data = load_model()
regressor = data["model"]
le_country = data["le_country"]
le_dev = data["le_dev"]
le_education = data["le_education"]

# Initialize CSV file
init_csv()


def show_predict_page():
    st.title("Salary Prediction")
    st.write("""### Please enter the required information to predict the salary""")

    # Define options
    countries = (
        "United States of America",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "India",
        "Canada",
        "France",
        "Brazil",
        "Spain",
        "Netherlands",
        "Poland",
        "Australia",
        "Italy",
        "Sweden",
        "Russian Federation",
        "Switzerland",
        "Turkey",
        "Israel",
        "Austria",
        "Portugal",
        "Norway",
        "Mexico",
    )

    dev_types = (
        "Developer, full-stack",
        "Developer, front-end",
        "Developer, back-end",
        "Data scientist or machine learning specialist",
        "Engineer, data",
        "Developer, mobile",
        "Developer, desktop or enterprise applications",
        "Engineer, site reliability",
        "Developer, embedded applications or devices",
        "Engineering manager",
        "DevOps specialist",
        "Developer, QA or test",
        "Academic researcher",
        "Data or business analyst",
        "Educator",
        "Senior Executive (C-Suite, VP, etc.)",
        "Developer, game or graphics",
        "Cloud infrastructure engineer",
    )

    education = (
        "Master's degree",
        "Bachelor's degree",
        "Less than a Bachelors",
        "Post grad",
    )

    # User input
    country = st.selectbox("Country", countries)
    dev_type = st.selectbox("Type of job", dev_types)
    education = st.selectbox("Education Level", education)
    experience = st.slider("Years of experience", 0, 50, 3)
    ok = st.button("Calculate Salary")

    if ok:
        # Prepare input data for prediction
        X = np.array([[country, dev_type, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_dev.transform(X[:, 1])
        X[:, 2] = le_education.transform(X[:, 2])
        X = X.astype(float)

        # Predict salary
        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:,.2f}")

        # Get user's IP address
        ip = socket.gethostbyname(socket.gethostname())

        # Log data
        log_user_data(ip, country, dev_type, education, experience, salary[0])

        # Optionally, display the IP and data for verification
        st.write(f"IP Address: {ip}")
        st.write(
            f"Country: {country}, Job Type: {dev_type}, Education: {education}, Experience: {experience}, Predicted Salary: ${salary[0]:,.2f}"
        )

    # st.write(
    #     """**DISCLAIMER:** The prediction is done using a survey data collected on stackoverflow in 2022 so the estimated salary is with respect to exchange rates at the time of the survey."""
    # )


show_predict_page()
