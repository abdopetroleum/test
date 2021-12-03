from django import forms
from .services import ConvertUnitService
from django.utils.html import conditional_escape as esc

def name_to_label(name:str):
    name = name.replace('_', ' ,')
    words = name.split(',')
    label = ''
    for word in words:
        label += word.capitalize()

    return label+':'

def name_to_placeholder(name:str):
    name = name.replace('_', ' ,')
    words = name.split(',')
    placeholder = ''
    for word in words:
        placeholder += word

    return placeholder

def name_to_tooltip(name:str, message:str=None):
    name = name.replace('_', ' ,')
    words = name.split(',')
    title = ''
    for word in words:
        title += word

    if message is not None:
        tooltip = message.format(title)
    else:
        tooltip = 'Please enter {} value'.format(title)

    return tooltip

class NumberInputWithUnit(forms.widgets.Input):
    template_name = 'widgets/number_input_with_unit.html'
    input_type = 'number'

    def get_context(self, name, value, attrs):
        name = esc(name)
        value = esc(value)
        context = super(NumberInputWithUnit, self).get_context(name, value, attrs)
        attributes = self.attrs
        
        additional_classes = ''
        if 'tooltip' in attributes and len(attributes['tooltip']):
            attributes['tooltip'] = esc(attributes['tooltip'])
            # additional_classes += ' hasTooltip'
        if 'required' in attributes and attributes['required'] == 'required':
            additional_classes += ' isRequired'
            context['widget']['required'] = 'required'
        else:
            del(context['widget']['required'])
            
        context['widget']['additional_classes'] = additional_classes

        if 'label' not in attributes:
            context['widget']['label'] = name_to_label(name)
        else:
            context['widget']['label'] = esc(attributes['label'])

        if 'placeholder' not in attributes:
            context['widget']['attrs']['placeholder'] = name_to_placeholder(name)
        else:
            context['widget']['attrs']['placeholder'] = esc(attributes['placeholder'])
        
        if 'tooltip' not in attributes:
            context['widget']['tooltip'] = name_to_tooltip(name)
        else:
            context['widget']['tooltip'] = esc(attributes['tooltip'])

        if 'needs_conversion' in attributes and not attributes['needs_conversion']:
            context['widget']['unit_name'] = name+'_unit_show'
        else:
            context['widget']['unit_name'] = name+'_unit'
        
        return context

        
class NumberInput(forms.widgets.Input):
    template_name = 'widgets/number_input.html'
    input_type = 'number'

    def get_context(self, name, value, attrs):
        context = super(NumberInput, self).get_context(esc(name), esc(value), attrs)
        attributes = self.attrs

        additional_classes = ''
        if 'tooltip' in attributes and len(attributes['tooltip']):
            attributes['tooltip'] = esc(attributes['tooltip'])
            # additional_classes += ' hasTooltip'
        if 'required' in attributes and attributes['required'] == 'required':
            additional_classes += ' isRequired'
            context['widget']['required'] = 'required'
        else:
            del(context['widget']['required'])

        context['widget']['additional_classes'] = additional_classes

        if 'label' not in attributes:
            context['widget']['label'] = name_to_label(name)
        else:
            context['widget']['label'] = esc(attributes['label'])

        if 'placeholder' not in attributes:
            context['widget']['attrs']['placeholder'] = name_to_placeholder(name)
        else:
            context['widget']['attrs']['placeholder'] = esc(attributes['placeholder'])
        
        if 'tooltip' not in attributes:
            context['widget']['tooltip'] = name_to_tooltip(name)
        else:
            context['widget']['tooltip'] = esc(attributes['tooltip'])
        
        return context

class Dropdown(forms.widgets.Select):
    template_name = 'widgets/select.html'
    option_template_name  = 'widgets/select_option.html'
    input_type = 'number'

    def get_context(self, name, value, attrs):
        name = esc(name)
        value = esc(value)
        context = super(Dropdown, self).get_context(name, value, attrs)
        attributes = self.attrs
        
        additional_classes = ''
        if 'tooltip' in attributes and len(attributes['tooltip']):
            attributes['tooltip'] = esc(attributes['tooltip'])
            # additional_classes += ' hasTooltip'
        if 'required' in attributes and attributes['required'] == 'required':
            additional_classes += ' isRequired'
            context['widget']['required'] = 'required'
        else:
            del(context['widget']['required'])

        context['widget']['additional_classes'] = additional_classes

        if 'label' not in attributes:
            context['widget']['label'] = name_to_label(name)
        else:
            context['widget']['label'] = esc(attributes['label'])

        if 'placeholder' not in attributes:
            context['widget']['attrs']['placeholder'] = 'choose one...'
        else:
            context['widget']['attrs']['placeholder'] = esc(attributes['placeholder'])
        
        if 'tooltip' not in attributes:
            context['widget']['tooltip'] = name_to_tooltip(name, 'Please choose {} from list')
        else:
            context['widget']['tooltip'] = esc(attributes['tooltip'])
        
        return context