
from django.http import HttpResponse
from django.conf import settings
import os
from django.template.loader import get_template
# Create your views here.

def _get_content(name):
    print(os.path.join(settings.BASE_DIR,'frontend', 'templates', 'frontend', name))
    with open(os.path.join(settings.BASE_DIR,'frontend', 'templates', 'frontend', name+'.html')) as fh:
        return fh.read()

def index(request, name='index'):
    template = get_template('index.html')
    return HttpResponse(template.render())

def about(request, name='about'):
    template = get_template('about.html')
    return HttpResponse(template.render())