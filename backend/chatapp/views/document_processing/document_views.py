from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Document 
from ...models import File
from .utils import *

@method_decorator(csrf_exempt, name='dispatch')
class DocumentProcessingView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """Process uploaded documents and store in File model"""
        try:
            # Get the uploaded file from the request
            uploaded_file = request.FILES.get('file')

            if not uploaded_file:
                return Response({"error": "File is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Determine file type and extract content
            file_type = uploaded_file.content_type
            extracted_text = ""
            file_name = uploaded_file.name
            
            # Save the file temporarily to process
            document = Document.objects.create(file=uploaded_file)
            file_path = document.file.path

            try:
                if file_type == 'text/csv':
                    # Process CSV file
                    result = process_csv(uploaded_file)
                    if "error" in result:
                        document.delete()
                        return Response(result, status=status.HTTP_400_BAD_REQUEST)
                    extracted_text = str(result)  # Convert CSV data to string
                
                elif file_type == 'application/pdf':
                    # Process PDF file
                    extracted_text = extract_text_from_pdf(file_path)
                
                elif file_type in ['image/png', 'image/jpeg', 'image/jpg']:
                    # Process Image file (for OCR)
                    result = process_image(uploaded_file)
                    if "error" in result:
                        document.delete()
                        return Response(result, status=status.HTTP_400_BAD_REQUEST)
                    extracted_text = result.get("text", "")
                    
                elif file_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
                    # Process Word documents (.docx and .doc)
                    extracted_text = extract_text_from_docx(file_path)
                    
                else:
                    # Delete the saved document if file type is unsupported
                    document.delete()
                    return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)

                # Save extracted content to File model for chatbot use
                file_obj = File.objects.create(
                    name=file_name,
                    content=extracted_text,
                    file_type=file_type
                )
                
                # Delete temporary document
                document.delete()

                return Response({
                    "message": "File processed successfully",
                    "file_id": file_obj.id,
                    "file_name": file_name,
                    "extracted_text_preview": extracted_text[:300],
                    "text_length": len(extracted_text)
                }, status=status.HTTP_200_OK)

            except Exception as e:
                document.delete()
                raise e

        except Exception as e:
            return Response({"error": f"Failed to process document: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        """Retrieve list of uploaded documents"""
        try:
            files = File.objects.all().order_by('-created_at').values(
                'id', 'name', 'file_type', 'created_at'
            )
            
            return Response({
                'documents': list(files),
                'count': len(files)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Failed to retrieve documents: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        """Delete a document - removes it from the chatbot's knowledge"""
        try:
            file_id = request.data.get('file_id')
            
            if not file_id:
                return Response({"error": "file_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                file_obj = File.objects.get(id=file_id)
                file_obj.delete()
                return Response({"message": "Document deleted successfully. Chatbot will no longer reference this document."}, status=status.HTTP_200_OK)
            except File.DoesNotExist:
                return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": f"Failed to delete document: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
