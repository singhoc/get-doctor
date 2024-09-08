import streamlit as st
from openai import OpenAI
import os

# Set up OpenAI API key
api_key = ""
# api_key = "fff"
client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key
)


# Function to read file contents
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to replace placeholders in a template
def replace_placeholder(template, placeholder, replacement):
    return template.replace(placeholder, replacement)

# Function to make OpenAI API call
def get_openai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("Medical Condition Detailer and Doctor Finder")

# Input from user
patient_description = st.text_area("Describe your symptoms:")

# Function to display doctor card
def display_doctor_card(doctor, index):
    st.markdown(f"""
        <div style="border:1px solid #ccc; border-radius:10px; padding:10px; margin:10px; text-align:center;">
            <h4>{doctor['name']}</h4>
            <p>ID: {doctor['id']}</p>
            <p>Specialization: {doctor['specialization']}</p>
            <p>Reason: {doctor['reason']}</p>
            <button style="padding: 5px 10px; border:none; border-radius:5px; background-color:#4CAF50; color:white;" onclick="window.location.href = '?book={index}'">Book Appointment</button>
        </div>
    """, unsafe_allow_html=True)


# Button to process the input
if st.button("Find Details and Doctor"):
    if patient_description:
        # Read templates
        detailer_template = read_file('detailer_prompt.txt')
        doctor_finder_template = read_file('doctor_finder_prompt.txt')
        doctors_list = read_file('doctors.txt')

        # Create detailed symptoms prompt
        detailed_symptoms_prompt = replace_placeholder(detailer_template, '[PATIENT_SYMPTOMS]', patient_description)
        print(detailed_symptoms_prompt)
        # Get detailed symptoms from OpenAI
        detailed_symptoms = get_openai_response(detailed_symptoms_prompt)

        # Create doctor finder prompt
        doctor_finder_prompt = replace_placeholder(doctor_finder_template, '[SYMPTOM_LIST]', detailed_symptoms)
        doctor_finder_prompt = replace_placeholder(doctor_finder_prompt, '[DOCTORS_LIST]', doctors_list)

        print(doctor_finder_prompt)

        # Get doctor suggestion from OpenAI
        doctor_suggestion = get_openai_response(doctor_finder_prompt)

        # Parse the doctor suggestion into a list of dictionaries
        print(doctor_suggestion)
        doctor_list = eval(doctor_suggestion)

        # Display results
        st.subheader("Detailed Symptoms")
        st.write(detailed_symptoms)

        st.subheader("Doctor Suggestion")
        if doctor_list:
            for i, doctor in enumerate(doctor_list):
                display_doctor_card(doctor, i)
        else:
            st.write("No doctors found.")
    else:
        st.warning("Please enter your symptoms.")