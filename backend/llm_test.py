import os
from google import genai
from extractor2 import process_cv
from utils import UPLOAD_FOLDER

# Initialize the Google Gemini client
client = genai.Client(api_key="AIzaSyDULtJo3j7h8kOkLYxCAqlWHEnKy4gFSAI")

# Check if extraction was successful
def compare_cv_and_job(cv_text, job_url):

    # get the text from url using the genai client
    # response = client.models.extract_text(url=job_url)
    # job_text = response.text

    # Use Gemini LLM to generate comparison text between the CV and the job description
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f" compare  Original Text: {cv_text}\n and Job URL: {job_url}\n and give suggestions",
    )

    # Step 3: Print the response from Gemini LLM
    print("Generated Content by Gemini LLM:")
    print(response.text)

    return response.text