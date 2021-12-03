from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()
esc = conditional_escape


@register.simple_tag
def numberInput(title, name, unit, min, max, value='', tooltip='', required=''):
    unitTag = ''
    if(len(unit) > 0):
        unitTag = '<span class="unit">{}</span>'.format(esc(unit))

    tooltipClass = ''
    if(len(tooltip)):
        tooltipClass = 'hasTooltip'

    result = '<div class="input-field__inline {}"><label for="{}"><span class="input-label" title="{}">{}</span><input {} id="{}" name="{}" type="number" min="{}" max="{}" value="{}" step="any">{}</label></div>'.format(tooltipClass, esc(name), esc(tooltip), esc(title), esc(required), esc(name), esc(name), min, max, value, unitTag)
    #                                   tooltipClass        name                            tooltip     title       required    name    name                    min     max         value        unitTag
    return mark_safe(result)