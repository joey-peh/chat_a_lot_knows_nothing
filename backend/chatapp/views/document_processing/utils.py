import fitz  # PyMuPDF for PDFs
import docx
import pandas as pd
from PIL import Image
import pytesseract
import pdfplumber

# Local Ollama library import (assuming you have a Python package or class for it)
import ollama  # or whatever the local Ollama package is

# Configuration - you should move this to settings.py
# OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Removed since no API call needed

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def process_csv(file):  # Removed 'self' parameter
    """Process CSV file and return data"""
    try:
        df = pd.read_csv(file)
        data = df.to_dict(orient="records")  # Convert dataframe to a list of records (dict)
        return {"message": "CSV processed successfully", "data": data}
    except Exception as e:
        return {"error": f"Failed to process CSV: {str(e)}"}

def process_pdf(file):  # Removed 'self' parameter
    """Process PDF file and extract text using pdfplumber"""
    try:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""  # Handle None return
        return {"message": "PDF processed successfully", "text": text}
    except Exception as e:
        return {"error": f"Failed to process PDF: {str(e)}"}

def process_image(file):  # Removed 'self' parameter
    """Process image file and extract text using OCR"""
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return {"message": "Image processed successfully", "text": text}
    except Exception as e:
        return {"error": f"Failed to process image: {str(e)}"}

def process_with_ollama(text, prompt):
    """Process text with the local Ollama library"""
    try:
        # Assuming Ollama has a function that takes context and prompt and returns a response
        response = ollama.chat(context=text, prompt=prompt)  # Replace with the actual method

        if response:
            return {"message": "Ollama processed successfully", "response": response}
        else:
            return {"error": "Failed to generate response from Ollama"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
