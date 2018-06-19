from django import template

register = template.Library()

@register.filter(name='subt')
def subt(value):
    return 5-int(value)


@register.filter(name='percent')
def percent(value, arg):
    try:
        percentage = (value/arg)*100
    except ZeroDivisionError:
        percentage = 0
    return percentage