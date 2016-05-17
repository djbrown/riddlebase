from django import template

register = template.Library()


@register.filter
def index(my_list: list, i: int):
    return my_list[int(i)]
