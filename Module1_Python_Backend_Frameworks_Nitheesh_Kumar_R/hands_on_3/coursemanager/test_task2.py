import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
django.setup()

from django.test import Client

client = Client()

print("Testing GET /api/courses/")
response = client.get('/api/courses/')
print("Status:", response.status_code)
if response.status_code != 200:
    import re
    m = re.search(r'(?s)Using the URLconf.*?The current path', response.content.decode('utf-8'))
    if m:
        print(m.group(0))

print("\nTesting GET /api/courses/1/students/")
response = client.get('/api/courses/1/students/')
print("Status:", response.status_code)
