from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()
esc = conditional_escape

@register.simple_tag
def dropDown(title, name, value = '', tooltip = ''):
    
    tooltipClass = ''
    if(len(tooltip)):
        tooltipClass = 'hasTooltip'
    
    result = '<div class="input-field__inline {}"><label for="{}"><span class="input-label" title="{}">{}</span><select id="{}" name="{}" type="number"></select></label></div>'.format(tooltipClass, esc(name), esc(tooltip), esc(title), esc(name),  esc(name))
    
    return mark_safe(result)