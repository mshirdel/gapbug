from django.template import Library

register = Library()


@register.filter(name="times")
def times(number):
    if number:
        return range(number)
