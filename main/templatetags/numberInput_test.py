from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from ast import literal_eval as strToDict

register = template.Library()
esc = conditional_escape


@register.simple_tag
def numberInput_test( label, name, units, units_name='', min='', max='', step='', value='', placeholder='', tooltip='', required=''):

    additional_classes = ''
    if len(tooltip):
        additional_classes += ' hasTooltip'
    if required=='required':
        additional_classes += ' isRequired'

    unit_select_options=''
    if len(units):
        units = strToDict(units)
        for unit in units:
            unit_select_options += '<option value="{}">{}</option>'.format(unit,units[unit])

    result = '<div class="input-field__inline {}">' \
             '<label for="{}">' \
             '<span class="input-label">{}</span>' \
             '<span class="tooltip">i<dfn><span>{}</span></dfn></span>' \
             '<input id="{}" type="number" name="{}" value="{}" min="{}" max="{}" step="{}" placeholder="{}">' \
             '<div class="unit unit__select"><select id="{}" name="{}" >{}</select>' \
             '</div>' \
             '</label>' \
             '</div>'.format(additional_classes, esc(name), esc(label), esc(tooltip), esc(name), esc(name), value, min, max, step, esc(placeholder), esc(units_name), esc(units_name), unit_select_options)

    return mark_safe(result)