# middleware.py
from django.shortcuts import render,redirect
from django.urls import reverse
from django.conf import settings
from django.http import FileResponse
import os
# class Custom404Middleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         if response.status_code == 404:
#             return render(request, '404.html', status=404)
#         return response

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # If 404 and media requested
        if response.status_code == 404 and request.path.startswith(settings.MEDIA_URL):
            # Get the first static directory path
            static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
            default_image_path = os.path.join(static_dir, 'assets', 'img', 'product.png')

            if os.path.exists(default_image_path):
                return FileResponse(open(default_image_path, 'rb'), content_type='image/png')

        # Regular 404 fallback for all other pages
        if response.status_code == 404:
            return render(request, '404.html', status=404)

        return response





