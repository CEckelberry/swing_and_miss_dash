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
model = GenerativeModel(model_name="gemini-1.0-pro-001")

def generate_gemini_content(prompt):
    # Define the user's prompt in a Content object
    user_prompt_content = Content(
        role="user",
        parts=[
            Part.from_text(prompt),
        ],
    )

    # Specify a function declaration for the prompt (if needed, can be customized)
    function_name = "generate_report_section"
    generate_report_section_func = FunctionDeclaration(
        name=function_name,
        description="Generate a section of a weekly baseball report",
        parameters={
            "type": "object",
            "properties": {"section": {"type": "string", "description": "Section of the report"}},
        },
    )

    # Define a tool that includes the above function declaration
    report_tool = Tool(
        function_declarations=[generate_report_section_func],
    )

    # Send the prompt and instruct the model to generate content using the Tool
    response = model.generate_content(
        user_prompt_content,
        generation_config=GenerationConfig(temperature=0),
        tools=[report_tool],
    )

    function_call = response.candidates[0].function_calls[0]
    if function_call.name == function_name:
        # Extract the arguments to use in your API call
        section = function_call.args["section"]

        # Here you can use your preferred method to make an API request to fetch additional data if needed

        # In this example, we'll simulate a response payload
        api_response = {"section": section, "content": "Generated content for the section"}

        # Return the API response to Gemini so it can generate a model response or request another function call
        response = model.generate_content(
            [
                user_prompt_content,  # User prompt
                response.candidates[0].content,  # Function call response
                Content(
                    parts=[
                        Part.from_function_response(
                            name=function_name,
                            response={
                                "content": api_response,  # Return the API response to Gemini
                            },
                        ),
                    ],
                ),
            ],
            tools=[report_tool],
        )

        return response.candidates[0].content
    else:
        return "Failed to generate content"
