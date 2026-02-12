import os
from pathlib import Path
from dotenv import load_dotenv
import subprocess


# Deal with filepaths.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(Path.joinpath(BASE_DIR, '.env'))
staticfiles_path = Path.joinpath(BASE_DIR, 'staticfiles')
static_path = Path.joinpath(BASE_DIR, 'static')
themes_filepath = Path.joinpath(BASE_DIR, 'staticfiles', 'themes.css')

# Create the file content.
css_content = f'''
:root {{
    --navbar-color: {os.getenv('NAVBAR_COLOR')};
    --primary-color: {os.getenv('PRIMARY_COLOR')};
    --secondary-color: {os.getenv('SECONDARY_COLOR')};
    --tertiary-color: {os.getenv('TERTIARY_COLOR')};
}}
'''

# Write the file. 
with open(themes_filepath, 'w') as file:
    file.write(css_content.strip())

# Log the action. 
print('Theme file generated')

# # Copy the favicon folder
# subprocess.run([
#     'cp', '-r', f'${static_path}/*', f'{staticfiles_path}/',
#     ])


# print('favicon folder copies to staticfiles)