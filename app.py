import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from utils.gpt_helpers import get_research, generate_outline, generate_article
from utils.document_processor import DocumentProcessor
from data.system_prompts import RESEARCH_ASSISTANT_PROMPT, ARTICLE_OUTLINE_PROMPT

# Load environment variables
load_dotenv()

# Configure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize DocumentProcessor
doc_processor = DocumentProcessor()

def main():
    # Page config
    st.set_page_config(
        page_title="Sequencr Content Generator",
        page_icon="🏗️",
        layout="wide"
    )

    # Header
    st.title("🏗️ Sequencr Content Generator")
    st.markdown("""
    Generate research-based article outlines for Sequencr content.
    """)

    # Sidebar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This tool helps generate content ideas and outlines for Sequencr using three specialized GPT assistants:
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
        - Includes executive summary and data points
        - Creates separate outlines for each research topic
        - Ensures technical depth and business relevance
        """)

        st.subheader("3. Brand Voice Assistant")
        st.markdown("""
        - Transforms outlines into polished articles
        - Maintains Brand's professional voice
        - Ensures technical accuracy
        - Incorporates brand guidelines
        - Produces publication-ready content
        """)

        st.divider()
        st.subheader("Knowledge Base Management")
        
        # URL input
        url_input = st.text_input("Add URL to knowledge base:")
        if st.button("Process URL"):
            if url_input:
                with st.spinner("Processing URL..."):
                    result = doc_processor.process_url(url_input)
                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(result["error"])
        
        # PDF upload
        uploaded_file = st.file_uploader("Upload PDF to knowledge base", type="pdf")
        if uploaded_file is not None:
            if st.button("Process PDF"):
                with st.spinner("Processing PDF..."):
                    result = doc_processor.process_pdf(uploaded_file)
                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(result["error"])
        
        # View knowledge base
        if st.button("View Knowledge Base"):
            st.json(doc_processor.knowledge_base)

    # Input section at the top
    st.subheader("Research Input")
    topic = st.text_area(
        "Enter a topic or area of interest:",
        placeholder="e.g., AI trends in 2024",
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

            # Final Article Phase
            with st.spinner("Generating article..."):
                article_result = generate_article(st.session_state.outline_data)
                if article_result["success"]:
                    st.session_state.article_data = article_result["data"]
                    st.success("Article generated!")
                else:
                    st.error(f"Article Error: {article_result['error']}")
                    return

    # Results section in two columns for Research and Outline
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

    # Final Article section below the columns
    st.subheader("Final Article")
    if "article_data" in st.session_state:
        # Add download button for the article
        st.download_button(
            label="Download Article",
            data=st.session_state.article_data,
            file_name="atkins_realis_article.md",
            mime="text/markdown"
        )
        # Display the article with proper formatting
        st.markdown(st.session_state.article_data)
    else:
        st.info("Final article will appear here...")

if __name__ == "__main__":
    main() 