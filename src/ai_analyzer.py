import json
from typing import List
from pydantic import BaseModel, Field
from openai import OpenAI

class MatchResult(BaseModel):
    score: int = Field(description="A score out of 100 representing how well the resume matches the job description.")
    matched_skills: List[str] = Field(description="A list of skills present in both the resume and the job description.")
    missing_skills: List[str] = Field(description="A list of skills required or preferred by the job description but missing from the resume.")
    explanation: str = Field(description="A brief paragraph explaining the reasoning behind the score.")

def analyze_resume_match(resume_text: str, job_description: str, api_key: str) -> dict:
    """
    Calls the OpenAI API to analyze the resume against the job description.
    Returns a dictionary containing the score, matched_skills, missing_skills, and explanation.
    """
    client = OpenAI(api_key=api_key)

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
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI that analyzes resumes against job descriptions and outputs structured JSON data."},
                {"role": "user", "content": prompt}
            ],
            response_format=MatchResult,
            temperature=0.2,
        )

        result = response.choices[0].message.parsed
        return result.model_dump()

    except Exception as e:
        raise Exception(f"Failed to analyze using OpenAI: {str(e)}")
