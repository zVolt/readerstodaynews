
from django.http import HttpResponse
from django.conf import settings
import os
# Create your views here.

def _get_content(name):
    with open(os.path.join(settings.BASE_DIR,'frontend', 'html', name)) as fh:
        return fh.read()

def index(request):
    return HttpResponse(_get_content('index.html'))