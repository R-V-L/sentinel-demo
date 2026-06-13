import sys
import os

# PythonAnywhere expects the WSGI application as 'application'
# Replace 'TU_USUARIO' with your PythonAnywhere username

# Uncomment and adjust if your project is at a different path:
# path = '/home/TU_USUARIO/sentinel-demo'
# if path not in sys.path:
#     sys.path.insert(0, path)

from app import app as application
