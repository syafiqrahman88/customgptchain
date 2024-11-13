from openai import OpenAI
from typing import Dict, Any
from data.system_prompts import RESEARCH_ASSISTANT_PROMPT, ARTICLE_OUTLINE_PROMPT

# Initialize the OpenAI client
client = OpenAI()

def get_research(topic: str) -> Dict[str, Any]:
    """Generate research results for given topic."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": RESEARCH_ASSISTANT_PROMPT
                },
                {
                    "role": "user",
                    "content": f"Research current trends and data related to: {topic}"
                }
            ],
            temperature=0.3
        )
        return {
            "success": True,
            "data": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def generate_outline(research_data: str) -> Dict[str, Any]:
    """Generate article outline based on research data."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": ARTICLE_OUTLINE_PROMPT
                },
                {
                    "role": "user",
                    "content": f"Create an article outline based on this research: {research_data}"
                }
            ],
            temperature=0.7
        )
        return {
            "success": True,
            "data": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        } 