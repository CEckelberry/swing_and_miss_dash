# gemini/gemini_api.py

import streamlit as st
from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)

# Credentials and client setup
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])

# Initialize Vertex AI
project_id = "swingandmiss"  # Replace with your project ID
vertexai.init(project=project_id, location="us-central1", credentials=credentials)

# Initialize Gemini model
model = GenerativeModel(model_name="gemini-1.5-pro")

def generate_gemini_content(prompt):
    # Define the user's prompt in a Content object
    user_prompt_content = Content(
        role="user",
        parts=[
            Part.from_text(prompt),
        ],
    )

    # Send the prompt and instruct the model to generate content
    response = model.generate_content(
        user_prompt_content,
        generation_config=GenerationConfig(temperature=0),
    )

    # Check if the response contains candidates
    if not response.candidates:
        return "No candidates found in the response"

    # Extract and return the generated text from the first candidate
    return response.candidates[0].content.parts[0].text if response.candidates[0].content.parts else "No content generated"