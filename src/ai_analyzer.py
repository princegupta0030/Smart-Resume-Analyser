import json
from typing import List
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class MatchResult(BaseModel):
    score: int = Field(description="A score out of 100 representing how well the resume matches the job description.")
    matched_skills: List[str] = Field(description="A list of skills present in both the resume and the job description.")
    missing_skills: List[str] = Field(description="A list of skills required or preferred by the job description but missing from the resume.")
    explanation: str = Field(description="A brief paragraph explaining the reasoning behind the score.")

def analyze_resume_match(resume_text: str, job_description: str, api_key: str) -> dict:
    """
    Calls the Gemini API to analyze the resume against the job description.
    Returns a dictionary containing the score, matched_skills, missing_skills, and explanation.
    """
    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an expert technical recruiter and resume analyzer.
    Compare the following Resume text to the provided Job Description.

    === Job Description ===
    {job_description}

    === Resume ===
    {resume_text}

    Analyze how well the candidate's resume matches the job description.
    """

    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
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
        raise Exception(f"Failed to analyze using Gemini: {str(e)}")
