# 代码生成时间: 2025-08-06 15:57:04
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import ExcelRecord
from .forms import ExcelUploadForm
from .utils import create_excel

class ExcelGeneratorView(View):
    def get(self, request):
        '''
        GET request handler for generating Excel file.
        Returns a response with the generated Excel file.
        '''
        # Retrieve the last generated Excel record
        last_record = ExcelRecord.objects.last()
        if last_record:
            # Create an Excel file using the stored data
            excel_file = create_excel(last_record.data)
            # Save the file to the storage system
            response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{last_record.filename}"'
            return response
        else:
            # Handle the case where there is no record
            return HttpResponse('No records to generate Excel file.', status=404)

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        '''
        POST request handler for uploading a CSV file to generate an Excel file.
        '''
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            uploaded_file = request.FILES['file']
            # Save the file to the storage system
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            # Store the file path in the model
            record = ExcelRecord.objects.create(filename=filename, data=fs.url(filename))
            # Generate the Excel file
            excel_file = create_excel(uploaded_file.read())
            # Return the Excel file as a response
            response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
            return response
        else:
            # Handle form errors
            return HttpResponse('Invalid form data.', status=400)
