import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

DEFAULT_MODEL = "openrouter/free"

MOVIE_SYSTEM_PROMPT = """
You are 'Cinephile AI', an expert movie critic and recommendation engine. 
You provide insightful, concise information about films, directors, and cinematography.
When asked for movie details, provide a compelling 2-3 sentence plot summary.
"""

def ask_ai(prompt: str, system_prompt: str = MOVIE_SYSTEM_PROMPT) -> str:
    """General purpose function to talk to the AI."""
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

def get_movie_details(title: str) -> dict:
    """Uses AI to get structured details about a movie based on its title."""
    prompt = f"Provide the following details for the movie '{title}' in a structured format: Genre, Rating (out of 10), and a 2-sentence Summary. Format the output clearly."
    response = ask_ai(prompt)
    return {"raw_response": response}
