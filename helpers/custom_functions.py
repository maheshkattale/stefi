
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from io import BytesIO
from django.core.files.storage import FileSystemStorage
import time
from .validations import hosturl
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from stefi.settings import *
import locale
from urllib.parse import urlparse, parse_qs
from datetime import datetime,date,timedelta
from PIL import Image, ImageDraw, ImageFont
from mimetypes import guess_type
from django.conf import settings
import logging
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework import pagination

from pathlib import Path

def format_indian_rupees(number):
    number=int(number)
    locale.setlocale(locale.LC_ALL, 'en_IN')
    return locale.format_string("%d", number, grouping=True)

def extract_lat_lng_from_url(google_maps_url):
    # Parse the URL
    parsed_url = urlparse(google_maps_url)
    # Extract the path and split by '/'
    path_segments = parsed_url.path.split('/')
    for segment in path_segments:
        if '@' in segment:  # Look for the segment with '@' containing coordinates
            coordinates = segment.split('@')[1].split(',')[:2]  # Get lat and lng
            latitude = coordinates[0]
            longitude = coordinates[1]
            return float(latitude), float(longitude)
    return None, None




def save_file(folder_path, uploaded_file, request):
    try:
        # Ensure the folder exists
        os.makedirs(folder_path, exist_ok=True)
        
        # Sanitize the filename
        filename = slugify(Path(uploaded_file.name).stem) + Path(uploaded_file.name).suffix
        file_path = os.path.join(folder_path, filename)

        # Validate MIME type
        mime_type, _ = guess_type(uploaded_file.name)
        if not mime_type:
            return {'msg': 'Invalid file type', 'url': '', 'n': 0}

        # Allowed file types
        allowed_types = ("image/", "video/", "application/pdf", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        if not any(mime_type.startswith(t) for t in allowed_types):
            return {'msg': 'Unsupported file type.', 'url': '', 'n': 0}

        # Save the uploaded file
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

    except Exception as e:
        logging.error(f"Failed to process the file: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
        return {'msg': f"Failed to process the file: {e}", 'url': '', 'n': 0}

    # Get the relative file path for the URL
    media_root_path = Path(settings.MEDIA_ROOT).resolve()
    file_path_resolved = Path(file_path).resolve()
    
    try:
        relative_file_path = file_path_resolved.relative_to(media_root_path)
    except ValueError:
        logging.error("File path is outside MEDIA_ROOT. Returning absolute URL.")
        relative_file_path = file_path_resolved  # Fall back to absolute path

    file_url = request.build_absolute_uri(settings.MEDIA_URL + str(relative_file_path).replace("\\", "/"))
    return {'msg': 'File saved successfully', 'url': file_url, 'n': 1}

from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.core.paginator import InvalidPage

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'

    def get_paginated_response(self, data):
        # Check if page exists before trying to access it
        if not hasattr(self, 'page'):
            return Response({
                "response": {"n": 1, "msg": "list fetched successfully", "status": "success"},
                'count': 0,
                'next': None,
                'previous': None,
                'data': data,
            })
        
        return Response({
            "response": {"n": 1, "msg": "list fetched successfully", "status": "success"},
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data,
        })
   


    def paginate_queryset(self, queryset, request, view=None):
        # For POST requests, get page number from request.data
        if request.method == 'POST' and hasattr(request, 'data'):
            self.page_size = request.data.get(self.page_size_query_param, self.page_size)
            page_number = request.data.get(self.page_query_param, 1)
        else:
            return super().paginate_queryset(queryset, request, view)
        
        paginator = self.django_paginator_class(queryset, self.page_size)
        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)


































































