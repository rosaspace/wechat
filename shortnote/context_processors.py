# myapp/context_processors.py

from django.conf import settings


def show_image(request):
    # Returns the SHOW_IMAGE variable to be available in the template context
    return {'showImage': settings.SHOW_IMAGE}
