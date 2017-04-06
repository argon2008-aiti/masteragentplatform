from django import template

register = template.Library()

@register.filter
def get_from_index(_list, index):
    return _list[index]
