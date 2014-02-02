from django import template
import datetime

register = template.Library()

# Turn a datetime.timedelta into a string
@register.filter(name='timedelta')
def timedelta(value):
    if not value:
        return "0"
    time = int(value / 1000000)
    delta = datetime.timedelta(0, time)
    return str(delta)
