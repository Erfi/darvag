from django import template

register = template.Library()

@register.filter
def get_tag_name(tag_instance):
    return tag_instance.name
