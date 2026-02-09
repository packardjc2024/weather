"""
This module sets the variables that can be used in any views context dictionary
for rendering templates, including base.html
"""


from datetime import datetime
from django.conf import settings


def add_global_context(request):
    """
    Adds a global context for use among all templates, especially base.html.
    """
    return {
        'site_title': 'Site Title',
        'copyright_name': 'Copyright Name',
        'copyright_year': datetime.now().year,
        'site_logo_url': 'site_pictures/logo.png',
        'use_account': settings.USE_ACCOUNT,
    }