"""
Adds and a new app to an existing django project. Must be run from the root 
directory of the django project. It will make all necessary changes to both
settings.py and project.urls.py.
"""


import subprocess
import re
from pathlib import Path
import os


###############################################################################
# Get user input for the app name
###############################################################################
APP_NAME = input('APP Name: ').strip().replace(' ', '_').lower()
# directory_prompt = f'You are currently in\n\t{os.getcwd()}\nIs this the django root? (y/n): '
# correct_directory = input(directory_prompt).strip().lower()
# if correct_directory == 'y':
#     pass
# else:
#     root_string = input('Absolute path of django root: ').strip().lower()
#     DJANGO_ROOT = Path(root_string)

###############################################################################
# Define necessary Paths
###############################################################################
DJANGO_ROOT = Path('web')
MANAGE_PATH = DJANGO_ROOT.joinpath('manage.py')
SETTINGS_PATH = DJANGO_ROOT.joinpath('project', 'settings.py')
URLS_PATH = DJANGO_ROOT.joinpath('project', 'urls.py')
APP_PATH = DJANGO_ROOT.joinpath(APP_NAME)
TEMPLATES_PATH = APP_PATH.joinpath('templates', APP_NAME)
INDEX_PATH = TEMPLATES_PATH.joinpath('index.html')
STATIC_PATH = APP_PATH.joinpath('static', APP_NAME)
JS_PATH = STATIC_PATH.joinpath(f'{APP_NAME}.js')
CSS_PATH = STATIC_PATH.joinpath(f'{APP_NAME}.css')
APP_URLS_PATH = APP_PATH.joinpath('urls.py')
APP_VIEWS_PATH = APP_PATH.joinpath('views.py')

###############################################################################
# Run django commands
###############################################################################
# Check if app already exists
settings_text = SETTINGS_PATH.read_text(encoding='utf-8')
match = re.search(r"INSTALLED_APPS\s*=\s*\[(.*?)\]", settings_text, re.DOTALL)
if match:
    apps_string = match.group(1)
    installed_apps = re.findall(r"'([^']*)'", apps_string)
else:
    print('no INSTALLED APPS found, exiting...')
    quit()

if APP_NAME in installed_apps:
    print(f'APP NAME {APP_NAME} already exists, exiting...')
    quit()

os.chdir(DJANGO_ROOT)
subprocess.run(['python3', 'manage.py', 'startapp', f'{APP_NAME}'])
os.chdir('..')

###############################################################################
# Make necessary changes at project level
###############################################################################
def update_list(file_path, list_name, appended_value):
    """
    Opens the file and then finds the list and appends the given value
    to the end of the list before saving the file. 
    """
    file_text = file_path.read_text(encoding='utf-8')
    pattern = (
        rf'({list_name}\s*=\s*\[)'
        r'([\s\S]*?)'
        r'(\]\s*)'
    )
    # replacement = rf"\1\2    '{appended_value}',\n\3"
    result = re.sub(pattern, replacement, file_text, count=1)
    file_path.write_text(result, encoding='utf-8')

# Add the app to settings.py
replacement = replacement = rf"\1\2    '{APP_NAME}',\n\3"
update_list(SETTINGS_PATH, 'INSTALLED_APPS', replacement)

# Add the app to urls.py
path_value = f"path('{APP_NAME}/', include('{APP_NAME}.urls'))"
replacement = rf"\1\2    {path_value},\n\3"
update_list(URLS_PATH, 'urlpatterns', replacement)


###############################################################################
# Create necessary files and directories
###############################################################################
# Create the templates and static folders
TEMPLATES_PATH.mkdir(parents=True, exist_ok=True)
INDEX_PATH.touch()
STATIC_PATH.mkdir(parents=True, exist_ok=True)
JS_PATH.touch()
CSS_PATH.touch()

# Write the app urls.py file and add the base
APP_URLS_PATH.touch()
app_urls_text = f"""
from django.urls import path
from . import views
from account.decorators import conditional_login_required


app_name = '{APP_NAME}'

urlpatterns = [
    path('', conditional_login_required(views.index), name='index'),
]
"""
with open(APP_URLS_PATH, 'w') as file:
    file.write(app_urls_text)

# Create the index view in the new app views.py
app_views_text = f"""
from django.shortcuts import render
from .models import *


def index(request):
    context = {{}}
    return render(request, '{APP_NAME}/index.html', context)
"""
with open(APP_VIEWS_PATH, 'w') as file:
    file.write(app_views_text)

# Create the base html in index.html
html_text = f"""
{{% extends 'base.html' %}}
{{% load static %}}


<!-- Add the static files to the header block -->
{{% block header_extension %}}
<link rel="stylesheet" type="text/css" href='{{% static "{APP_NAME}/{APP_NAME}.css" %}}'>
<script type="text/javascript" src="{{% static '{APP_NAME}/{APP_NAME}.js' %}}"></script>
{{% endblock %}}


<!-- Add the index's content to the main header block -->
{{% block body_extension %}}

<p>{APP_NAME} page under construction.</p>

{{% endblock %}}
"""
with open(INDEX_PATH, 'w') as file:
    file.write(html_text)