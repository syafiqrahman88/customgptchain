from openai import OpenAI
from typing import Dict, Any
from data.system_prompts import RESEARCH_ASSISTANT_PROMPT, ARTICLE_OUTLINE_PROMPT, BRAND_VOICE_PROMPT
from .document_processor import DocumentProcessor

# Initialize the OpenAI client
client = OpenAI()

# Initialize document processor
doc_processor = DocumentProcessor()

def get_research(topic: str) -> Dict[str, Any]:
    """Generate research results for given topic."""
    try:
        response = client.chat.completions.create(
            model="o1-mini",
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
            model="o1-mini",
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

def generate_article(outline_data: str) -> Dict[str, Any]:
    """Generate full article based on the outline and knowledge base."""
    try:
        # Get stored knowledge
        knowledge_base = doc_processor.get_combined_knowledge()
        
        # Create enhanced prompt
        enhanced_prompt = f"""
        {BRAND_VOICE_PROMPT}
        
        Reference Materials:
        {knowledge_base}
        
        Use the above reference materials to match the writing style and tone.
        """
        
        response = client.chat.completions.create(
            model="o1-mini",
            messages=[
                {
                    "role": "system",
                    "content": enhanced_prompt
                },
                {
                    "role": "user",
                    "content": f"Transform this outline into a complete article: {outline_data}"
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