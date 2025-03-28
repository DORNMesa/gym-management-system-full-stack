from django import template

register = template.Library()

@register.filter(name='report_subtract')
def subtract(value, arg):
    """Subtracts arg from value with float conversion and error handling"""
    try:
        return float(value or 0) - float(arg or 0)
    except (ValueError, TypeError):
        return 0




