from django import template
from django.template.defaultfilters import stringfilter
from member.models import Person

register = template.Library()

@register.filter
@stringfilter
def mask_sender(value):
    mask = '0' + value[3:]
    name = _get_sender(mask)
    if name == '':
        name = _get_sender(value)
    
    if name != '':
        name = '(%s)' % name
        
    return name

def _get_sender(phone):
    result = ''
    try:
        person = Person.objects.get(no_handphone=phone)
        result = person.nama_lengkap
    except:
        pass
    
    return result

