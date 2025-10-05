# 代码生成时间: 2025-10-06 03:08:23
import os
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
def generate_key():
    """Generate a key for encryption/decryption."""
    return Fernet.generate_key()

class EncryptionUtility:
    """Utility class for file encryption and decryption."""
    def __init__(self, key=None):
        self.key = key or generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, file_content):
        """Encrypts a file content."""
        return self.cipher_suite.encrypt(file_content.encode()).decode()

    def decrypt(self, encrypted_content):
        """Decrypts an encrypted content."""
        return self.cipher_suite.decrypt(encrypted_content.encode()).decode()

class FileEncryptionView(View):
    """View to handle file encryption/decryption requests."""
    def post(self, request):
        try:
            data = request.POST
            file_content = data.get('file_content')
            action = data.get('action')
            encryption_util = EncryptionUtility(key=settings.SECRET_KEY)

            if action == 'encrypt':
                encrypted_content = encryption_util.encrypt(file_content)
            elif action == 'decrypt':
                encrypted_content = data.get('encrypted_content')
                decrypted_content = encryption_util.decrypt(encrypted_content)
                return JsonResponse({'decrypted_content': decrypted_content})
            else:
                raise ValueError("Invalid action. Use 'encrypt' or 'decrypt'.")

            return JsonResponse({'encrypted_content': encrypted_content})
        except (ValueError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)

# urls.py
from django.urls import path
from .views import FileEncryptionView

urlpatterns = [
    path('encrypt/', FileEncryptionView.as_view(), name='file-encryption'),
]
