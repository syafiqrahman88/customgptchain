import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from utils.gpt_helpers import get_research, generate_outline
from data.system_prompts import RESEARCH_ASSISTANT_PROMPT, ARTICLE_OUTLINE_PROMPT

# Load environment variables
load_dotenv()

# Configure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    # Page config
    st.set_page_config(
        page_title="AtkinsRéalis Content Generator",
        page_icon="🏗️",
        layout="wide"
    )

    # Header
    st.title("🏗️ AtkinsRéalis Content Generator")
    st.markdown("""
    Generate research-based article outlines for AtkinsRéalis content.
    """)

    # Sidebar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This tool helps generate content ideas and outlines for AtkinsRéalis using two specialized GPT assistants:
        """)
        
        st.subheader("1. Research Assistant")
        st.markdown("""
        - Focuses on gathering relevant industry insights
        - Specializes in engineering and infrastructure topics
        - Structures data into digestible formats
        - Ensures data comes from reputable sources
        """)

        st.subheader("2. Outline Specialist")
        st.markdown("""
        - Transforms research into structured article outlines
        - Maintains consistent AtkinsRéalis voice
        - Creates separate outlines for each research topic
        - Ensures technical depth and business relevance
        """)

        st.subheader("Benefits")
        st.markdown("""
        - **Specialized Expertise**: Each assistant is optimized for its specific task
        - **Consistent Output**: Standardized format across all content
        - **Efficient Workflow**: Reduces manual research and structuring time
        - **Quality Control**: Built-in industry focus and source verification
        - **Scalable Content**: Easy to generate multiple outlines from single research
        """)

    # Input section at the top
    st.subheader("Research Input")
    topic = st.text_area(
        "Enter a topic or area of interest:",
        placeholder="e.g., sustainable infrastructure trends in 2024",
        height=100
    )

    if st.button("Generate Content", type="primary"):
        if topic:
            # Research Phase
            with st.spinner("Researching topics..."):
                research_result = get_research(topic)
                
                if research_result["success"]:
                    st.session_state.research_data = research_result["data"]
                    st.success("Research completed!")
                else:
                    st.error(f"Research Error: {research_result['error']}")
                    return

            # Outline Phase
            with st.spinner("Generating outline..."):
                outline_result = generate_outline(st.session_state.research_data)
                
                if outline_result["success"]:
                    st.session_state.outline_data = outline_result["data"]
                    st.success("Outline generated!")
                else:
                    st.error(f"Outline Error: {outline_result['error']}")
                    return

    # Results section in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Research Results")
        if "research_data" in st.session_state:
            st.markdown(st.session_state.research_data)
        else:
            st.info("Research results will appear here...")

    with col2:
        st.subheader("Article Outline")
        if "outline_data" in st.session_state:
            st.markdown(st.session_state.outline_data)
        else:
            st.info("Article outline will appear here...")

if __name__ == "__main__":
    main() 