import pandas as pd
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
import pytesseract
import pdfplumber

from .models import Document  # Assuming you have a Document model for file storage

class DocumentProcessingView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Get the uploaded file from the request
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        # Save the file if you want to store it in the database (optional)
        document = Document.objects.create(file=uploaded_file)

        # Process the file based on its type
        file_type = uploaded_file.content_type

        if file_type == 'text/csv':
            # Process CSV file
            return self.process_csv(uploaded_file)
        
        elif file_type == 'application/pdf':
            # Process PDF file
            return self.process_pdf(uploaded_file)
        
        elif file_type in ['image/png', 'image/jpeg']:
            # Process Image file (for OCR)
            return self.process_image(uploaded_file)
        
        else:
            return JsonResponse({"error": "Unsupported file type"}, status=400)

    def process_csv(self, file):
        # Read the CSV file using pandas
        try:
            df = pd.read_csv(file)
            data = df.to_dict(orient="records")  # Convert dataframe to a list of records (dict)
            return JsonResponse({"message": "CSV processed successfully", "data": data})
        except Exception as e:
            return JsonResponse({"error": f"Failed to process CSV: {str(e)}"}, status=500)

    def process_pdf(self, file):
        # Extract text from PDF using pdfplumber
        try:
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
            return JsonResponse({"message": "PDF processed successfully", "text": text})
        except Exception as e:
            return JsonResponse({"error": f"Failed to process PDF: {str(e)}"}, status=500)

    def process_image(self, file):
        # Extract text from image using Tesseract OCR
        try:
            image = Image.open(file)
            text = pytesseract.image_to_string(image)
            return JsonResponse({"message": "Image processed successfully", "text": text})
        except Exception as e:
            return JsonResponse({"error": f"Failed to process image: {str(e)}"}, status=500)
