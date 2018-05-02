from django import template
import re

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

#https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/
@register.filter(needs_autoescape=True)
def profil_link(text, autoescape=True):
    #first, other = text[0], text[1:]
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    #a = re.sub(r'@([a-zA-Z0-9_\-\+\@\.]+)', r'<strong>@<a href="">'+esc(r'\1')+'</a></strong>', text)
    b = esc(text)
    c = re.sub(r'@([a-zA-Z0-9_\-]+)', r'<strong>@<a href="http://papersoccer.pl/kibic/'+esc(r'\1')+'/">'+esc(r'\1')+'</a></strong>', b)
    #result = '<strong>%s</strong>%s' % (esc(a), esc(a))
    return mark_safe(c)
