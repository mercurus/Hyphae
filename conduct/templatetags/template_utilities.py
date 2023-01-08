import re, random
from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe
from widget_tweaks.templatetags.widget_tweaks import render_field
register = Library()


@register.tag
def input(parser, token): 
    """
    https://github.com/jazzband/django-widget-tweaks
    Hijack/rename tag from 'render_field' to 'input'
    Also makes it so we only need to load one thing: template_utilities
    """
    return render_field(parser, token)


#useage: {{ model_obj|readable:'enum_field_name' }}
@register.filter 
def readable(record, field_name):
    #get the EnumField so we have its Enumeration, then return full text
    enum_field = getattr(type(record), '_meta').get_field(field_name)
    return enum_field.readable(getattr(record, field_name))


#https://push.cx/2007/django-template-tag-for-dictionary-access {{ dictionary|hash:'key' }}
@register.filter
def hash(dictionary, key):
    if not type(dictionary) is dict:
        print(type(dictionary))
        raise TemplateSyntaxError('The hash filter requires a dictionary')
    if not key in dictionary:
        return ''
    return dictionary[key]


#https://stackoverflow.com/a/51556439
@register.filter
def get_fields(obj):
    if type(obj) is dict:
        return obj.items()
    return [(field.name, field.value_from_object(obj)) for field in obj._meta.fields]
    # return [(field.name, field.value_to_string(obj)) for field in obj._meta.fields]


#https://stackoverflow.com/a/12028864
@register.filter
def get_type(value):
    return re.search(r'\'(.+)\'', str(type(value))).group(1)
    # return type(value)


# https://stackoverflow.com/a/47401460
@register.filter
def modulo(num, val):
    return num % val


#https://stackoverflow.com/a/34572799  {% if request.user|has_group:'mygroup' %} 
# @register.filter
# def has_group(user, group_name):
#     return user.groups.filter(name=group_name).exists() 


#https://djangosnippets.org/snippets/539/
class AssignNode(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''


# {% assign [name] [value] %}
@register.tag
def assign(parser, token):
    """
    Assign an expression to a variable in the current context.
    """
    bits = token.split_contents()
    # print(bits[2])
    if len(bits) != 3:
        raise TemplateSyntaxError('{} tag takes two arguments'.format(bits[0]))
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)


#https://stackoverflow.com/a/23783666
@register.filter
def concat(arg1, arg2):
    return str(arg1) + str(arg2)


@register.simple_tag
def icon(icon_class='', extra_classes=''):
    icon_class = str(icon_class) or 'fas fa-globe'
    return mark_safe('<span class="icon {}"><i class="{}"></i></span>'.format(extra_classes, icon_class))


@register.simple_tag
def random_int(low, high=None):
    if not high:
        high = low
        low = 0
    return random.randint(low, high)
