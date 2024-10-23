from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    print(indexable)
    return indexable[i]