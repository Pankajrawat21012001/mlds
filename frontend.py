import streamlit as st
import requests
import pandas as pd
import os

st.title("Retail Analytics CoPilot")

# File upload
uploaded_file = st.file_uploader("Upload your sales data (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the uploaded file
    try:
        # Get the file name without the additional timestamp
        file_name = uploaded_file.name.split('|')[0]  # Extract the actual file name
        st.write(f"Uploaded file name: {file_name}")

        if file_name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif file_name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a CSV or Excel file.")
            st.stop()

        st.write("Data Preview:")
        st.dataframe(df)

        # Analyze button
        if st.button("Analyze"):
            # Change the URL to localhost
            response = requests.post("http://localhost:8000/uploadfile/", files={"file": uploaded_file})
            
            if response.status_code == 200:
                result = response.json()
                st.write("Analysis Result:")
                st.json(result)
            else:
                st.error("Error: " + response.json().get("error", "Unknown error"))

    except Exception as e:
        st.error(f"An error occurred: {e}")