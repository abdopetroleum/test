from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from ast import literal_eval as strToDict

register = template.Library()
esc = conditional_escape

@register.simple_tag
def dropDown_test(label, name, options, placeholder='', tooltip='', required=''):
    
    additional_classes = ''
    if len(tooltip):
        additional_classes += ' hasTooltip'
    if required == 'required':
        additional_classes += ' isRequired'

    optionTags = ''
    if len(options):
        # options = strToDict(options)
        for option in options:
            optionTags += '<option value="{}">{}</option>'.format(option,options[option])

    result = '<div class="input-field__inline input__select {}">' \
             '<label for="{}">' \
             '<span class="input-label">{}</span>' \
             '<span class="tooltip">i<dfn><span>{}</span></dfn></span>' \
             '<select id="{}" name="{}">' \
             '<option value="0">{}</option>{}</select>' \
             '</label>' \
             '</div>'.format(additional_classes, esc(name), esc(label), esc(tooltip), esc(name),
                             esc(name), esc(placeholder), optionTags)
    

    return mark_safe(result)