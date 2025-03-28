from django import template

register = template.Library()

@register.filter(name='member_abs')
def abs_val(value):
    """Returns the absolute value with error handling"""
    try:
        return abs(value)
    except (TypeError, ValueError):
        return value
