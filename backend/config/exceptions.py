from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        if isinstance(exc, ValidationError):
            response.data = {
                'success': False,
                'message': 'Validation failed.',
                'errors': response.data
            }
        else:
            # Handle other DRF exceptions (e.g. AuthenticationFailed, PermissionDenied)
            detail = response.data.get('detail', 'An error occurred.')
            response.data = {
                'success': False,
                'message': detail,
                'errors': response.data
            }
    return response
