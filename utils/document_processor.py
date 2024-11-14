import requests
from bs4 import BeautifulSoup
import PyPDF2
import io
import json
import os
from typing import List, Dict
import datetime

class DocumentProcessor:
    def __init__(self):
        self.knowledge_base_path = "data/knowledge_base.json"
        self.load_knowledge_base()

    def load_knowledge_base(self):
        """Load existing knowledge base or create new one"""
        if os.path.exists(self.knowledge_base_path):
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
        else:
            self.knowledge_base = {
                "urls": {},
                "pdf_content": {}
            }

    def save_knowledge_base(self):
        """Save knowledge base to file"""
        with open(self.knowledge_base_path, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, indent=4)

    def process_url(self, url: str) -> Dict:
        """Extract and process content from URL"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract main content (adjust selectors based on target websites)
            content = soup.find('article') or soup.find('main') or soup.find('body')
            
            # Clean and store content
            cleaned_content = ' '.join(content.stripped_strings)
            
            # Store in knowledge base
            self.knowledge_base["urls"][url] = {
                "content": cleaned_content,
                "timestamp": str(datetime.datetime.now())
            }
            self.save_knowledge_base()
            
            return {"success": True, "message": f"Successfully processed URL: {url}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def process_pdf(self, pdf_file) -> Dict:
        """Process and store PDF content"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
            content = ""
            
            for page in pdf_reader.pages:
                content += page.extract_text() + "\n"
            
            # Store in knowledge base
            filename = pdf_file.name
            self.knowledge_base["pdf_content"][filename] = {
                "content": content,
                "timestamp": str(datetime.datetime.now())
            }
            self.save_knowledge_base()
            
            return {"success": True, "message": f"Successfully processed PDF: {filename}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_combined_knowledge(self) -> str:
        """Combine all stored knowledge into a single string"""
        combined = []
        
        # Add URL content
        for url, data in self.knowledge_base["urls"].items():
            combined.append(f"Content from {url}:\n{data['content']}\n")
            
        # Add PDF content
        for filename, data in self.knowledge_base["pdf_content"].items():
            combined.append(f"Content from {filename}:\n{data['content']}\n")
            
        return "\n\n".join(combined) 