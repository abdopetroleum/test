from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()
esc = conditional_escape


@register.simple_tag
def error_messages(errors):

    error_spans=''
    if len(errors):
        for error in errors:
            error_spans += '<span>{}</span>'.format(esc(error))

    result = '<span class="error-messages">{}</span>'.format(error_spans)

    return mark_safe(result)