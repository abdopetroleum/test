from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()
esc = conditional_escape

@register.simple_tag
def headline(title):
    result = '<div class="headline"><span class="title">{}</span><span class="dash"></span></div>'.format(esc(title))
    return mark_safe(result)