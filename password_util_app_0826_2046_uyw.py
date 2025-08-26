# 代码生成时间: 2025-08-26 20:46:39
# Password Encryption and Decryption Utility
#
# This Django app provides utility functions to encrypt and decrypt passwords.
# It follows Django's best practices and includes models, views, and urls.
#
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from cryptography.fernet import Fernet


class PasswordUtils:
    """
    Utility class for password encryption and decryption.
    """
    def __init__(self):
        # Load the secret key from Django settings
        self.key = settings.SECRET_KEY
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, password):
        """
        Encrypt a password.
        :param password: The password to be encrypted.
        :return: The encrypted password.
        """
        return self.cipher_suite.encrypt(password.encode()).decode()

    def decrypt(self, encrypted_password):
        """
        Decrypt an encrypted password.
        :param encrypted_password: The encrypted password to be decrypted.
        :return: The decrypted password.
        """
        try:
            return self.cipher_suite.decrypt(encrypted_password.encode()).decode()
        except Exception as e:
            raise ValidationError(f"Error decrypting password: {e}")

# Models
# Since this is a utility app, we do not need models.

# Views
@csrf_exempt
@require_http_methods(['POST'])
def encrypt_password_view(request):
    """
    View to handle password encryption requests.
    """
    try:
        password = request.POST.get('password')
        if not password:
            return JsonResponse({'error': 'Password is required'}, status=400)

        password_utils = PasswordUtils()
        encrypted_password = password_utils.encrypt(password)
        return JsonResponse({'encrypted_password': encrypted_password})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['POST'])
def decrypt_password_view(request):
    """
    View to handle password decryption requests.
    """
    try:
        encrypted_password = request.POST.get('encrypted_password')
        if not encrypted_password:
            return JsonResponse({'error': 'Encrypted password is required'}, status=400)

        password_utils = PasswordUtils()
        decrypted_password = password_utils.decrypt(encrypted_password)
        return JsonResponse({'decrypted_password': decrypted_password})
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# URLs
from django.urls import path

urlpatterns = [
    path('encrypt/', encrypt_password_view, name='encrypt_password'),
    path('decrypt/', decrypt_password_view, name='decrypt_password'),
]
