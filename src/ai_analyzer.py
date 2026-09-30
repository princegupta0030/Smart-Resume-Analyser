import json
from typing import List
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class MatchResult(BaseModel):
    candidate_name: str = Field(description="The full name of the candidate extracted from the resume. Use 'Unknown' if not found.")
    candidate_email: str = Field(description="The email address of the candidate extracted from the resume. Use 'Unknown' if not found.")
    social_links: List[str] = Field(description="A list of URLs (LinkedIn, GitHub, Portfolio) found in the resume. Return an empty list if none are found.")
    match_score: int = Field(description="A score out of 100 representing how well the resume matches the job description.")
    matched_skills: List[str] = Field(description="A list of skills present in both the resume and the job description.")
    missing_skills: List[str] = Field(description="A list of skills required or preferred by the job description but missing from the resume.")
    short_summary: str = Field(description="A brief paragraph explaining the reasoning behind the score.")

def analyze_resume_match(resume_text: str, job_description: str, api_key: str) -> dict:
    """
    Calls the Gemini API to analyze the resume against the job description.
    Returns a dictionary containing candidate_name, candidate_email, social_links, match_score, matched_skills, missing_skills, and short_summary.
    """
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

    prompt = f"""
    You are an expert technical recruiter and resume analyzer.
    Compare the following Resume text to the provided Job Description.

    First, extract the candidate's name, email address, and any social links (LinkedIn, GitHub, Portfolio URLs) from their resume.
    Then, analyze how well the candidate's resume matches the job description.

    === Job Description ===
    {job_description}

    === Resume ===
    {resume_text}
    """

    # List of fallback models to try if one is experiencing high demand
    # Prioritize 3.8 and 3.7 series first as requested, then fallback to others.
    models_to_try = [
        'gemini-3.8-flash',
        'gemini-3.7-flash',
        'gemini-3.6-flash',
        'gemini-3.5-flash',
        'gemini-3.5-flash-lite',
        'gemini-flash-latest',
        'gemini-flash-lite-latest'
    ]

    last_error = None

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=MatchResult,
                    temperature=0.2,
                ),
            )

            # Parse the structured JSON response
            text = response.text
            try:
                data = json.loads(text)
            except json.JSONDecodeError as e:
                # Fallback if extra text exists (as per knowledgebase gotcha)
                data = json.loads(text[:e.pos])

            return data

        except Exception as e:
            last_error = str(e)
            # If it's a 503 or 429 error, it's a server overload, so continue to the next model
            if '503' in last_error or '429' in last_error:
                continue
            # If it's some other error (like a 400 or 404), continue anyway to try other fallbacks
            continue

    # If all models in the loop fail, raise an exception
    raise Exception(f"Failed to analyze using Gemini after trying multiple models. Last error: {last_error}")
