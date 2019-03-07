from django import template
from richtext_poc import helpers

register = template.Library()


@register.filter(name="render_markdown")
def render_markdown(value):
    return helpers.render_markdown(value)
