"""
Custom middleware for Content Security Policy (CSP) headers.

This middleware adds CSP headers to responses to help prevent XSS attacks
by specifying which domains can be used to load resources.
"""


class CSPMiddleware:
    """
    Middleware to add Content Security Policy headers.
    
    CSP helps prevent XSS attacks by controlling which resources
    (scripts, styles, images, etc.) can be loaded by the browser.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Basic Content Security Policy
        # Adjust these policies based on your application's needs
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "  # 'unsafe-inline' needed for Django admin
            "style-src 'self' 'unsafe-inline'; "   # 'unsafe-inline' needed for Django admin
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"  # Prevents framing (clickjacking protection)
        )
        
        response['Content-Security-Policy'] = csp_policy
        
        # Additional security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        return response

