"""
Custom CSRF Middleware untuk API endpoints
Disable CSRF protection untuk semua endpoint yang dimulai dengan /api/
"""

class CSRFExemptAPIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Disable CSRF untuk semua API endpoints
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        
        response = self.get_response(request)
        return response
