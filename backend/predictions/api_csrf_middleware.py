"""
Custom CSRF Middleware untuk disable CSRF protection pada API endpoints
"""

class DisableCSRFMiddleware:
    """
    Disable CSRF protection untuk semua API endpoints
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Disable CSRF untuk semua endpoint yang mengandung 'api'
        if '/api/' in request.path or request.path.startswith('/api'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Additional check untuk view-level CSRF disable
        if '/api/' in request.path or request.path.startswith('/api'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None
