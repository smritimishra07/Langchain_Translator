import requests
import streamlit as st

def get_groq_response(input_text):
    # Correctly use the input_text variable in the JSON body
    json_body = {
        "input": {
            "language": "French",
            "text": input_text  # Use the variable directly
        },
        "config": {},
        "kwargs": {}
    }
    # Send POST request to the API
    response = requests.post("http://127.0.0.1:8000/chain/invoke", json=json_body)

    # Check if the request was successful
    if response.status_code == 200:
        response_json = response.json()
        output = response_json.get("output", "No output field in response")
    else:
        output = f"Error: {response.status_code}, {response.text}"

    return output

# Streamlit app
st.title("LLM Application Using LCEL")
input_text = st.text_input("Enter the text you want to convert to French:")

if input_text:
    result = get_groq_response(input_text)
    st.write(result)