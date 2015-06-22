from django.contrib.staticfiles import finders
from django import template
import random, string

register = template.Library()

@register.filter
def get_range(value):
    return range(value)

@register.filter
def get_random_range(value):
    return range(random.randint(1,value))

@register.simple_tag
def random_number(min=10, max=256):
    return random.randint(min,max)

@register.simple_tag
def random_string(size=10):
    return ''.join(random.choice(string.lowercase) for i in range(size))

@register.simple_tag
def random_real_word(title=False):
    words = finders.find('OFTENMIS.TXT')
    if title:
        return random.choice(open(words).readlines()).title()
    else:
        return random.choice(open(words).readlines())
    
    