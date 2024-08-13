import streamlit as st
import pandas as pd
import os

# File path for the CSV file
csv_file = "data/Salaries.csv"

# Load existing data or create a new DataFrame
if os.path.exists(csv_file):
    data = pd.read_csv(csv_file)
else:
    data = pd.DataFrame(columns=["YearsExperience", "Degree", "Salary"])

# Streamlit app title
st.title("Wage Salary Predictor")

# Form to enter new salary data
st.header("Enter New Salary Data")
with st.form(key="salary_form"):
    years_experience = st.number_input(
        "Years of Experience", min_value=0, max_value=50, step=1
    )
    degree = st.selectbox("Degree", ["Bachelors", "Masters", "PhD"])
    salary = st.number_input("Salary", min_value=30000, max_value=500000, step=1000)
    submit_button = st.form_submit_button(label="Submit")

    # If the user submits the form, save the data to the CSV file
    if submit_button:
        new_entry = {
            "YearsExperience": years_experience,
            "Degree": degree,
            "Salary": salary,
        }
        data = data.append(new_entry, ignore_index=True)
        data.to_csv(csv_file, index=False)
        st.success("Data submitted successfully!")

# Display the existing data in the CSV file
st.header("Current Data in the Salaries.csv File")
st.dataframe(data)
