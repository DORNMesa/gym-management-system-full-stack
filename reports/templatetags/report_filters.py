from django import template

register = template.Library()

@register.filter(name='report_subtract')
def subtract(value, arg):
    """Subtracts arg from value with float conversion and error handling"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0



