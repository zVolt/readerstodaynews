from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import intcomma

from jinja2 import Environment

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'intcomma': intcomma
    })
    return env