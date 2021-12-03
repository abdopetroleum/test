from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from ast import literal_eval as strToDict

register = template.Library()
esc = conditional_escape


@register.simple_tag
def doubleRangeSlider(label, first_input_name, second_input_name, units, units_name='', min='', max='', step='', first_input_value='', second_input_value='', tooltip='', required=''):

    additional_classes = ''
    if len(tooltip):
        additional_classes += ' hasTooltip'
    if required == 'required':
        additional_classes += ' isRequired'

    unit_select_options = ''
    if len(units):
        units = strToDict(units)
        for unit in units:
            unit_select_options += '<option value="{}">{}</option>'.format(unit, units[unit])

    result = '<div class="input-field__inline {}">' \
             '<label for="{}">' \
             '<span class="input-label">{}</span>' \
             '<span class="tooltip">i<dfn><span>{}</span></dfn></span>' \
             '</label>' \
             '<div class="rangeSlider_doubleHandled">' \
             '<input id="{}" name="{}" type="number" value="{}" min="{}" max="{}" step="{}">' \
             '<div doubleslider class="slider-distance">' \
             '<div>' \
             '<div inverse-left></div>' \
             '<div inverse-right></div>' \
             '<div range></div>' \
             '<span thumb></span>' \
             '<span thumb></span>' \
             '<div sign>' \
             '<span></span>' \
             '</div>' \
             '<div sign>' \
             '<span></span>' \
             '</div>' \
             '</div>' \
             '<input type="range" tabindex="0"/>' \
             '<input type="range" tabindex="0"/>' \
             '</div>' \
             '<input id="{}" name="{}" type="number" value="{}">' \
             '<div class="unit unit__select">' \
             '<select id="{}" name="{}" >{}</select>' \
             '</div>' \
             '</div>' \
             '</div>'.format(additional_classes, esc(first_input_name), esc(label), esc(tooltip),
                             esc(first_input_name), esc(first_input_name), first_input_value, min, max, step,
                             esc(second_input_name), esc(second_input_name), second_input_value,
                             esc(units_name), esc(units_name), unit_select_options)

    return mark_safe(result)