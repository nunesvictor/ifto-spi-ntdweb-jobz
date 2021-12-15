from typing import List

from core import mask_utils
from django import template

register = template.Library()


@register.filter
def mask(value, type):
    mask_callable = getattr(mask_utils, f'mask_{type}')

    if mask_callable:
        return mask_callable(value)


class isCurrentNode(template.Node):
    def __init__(self, patterns: List[str], output: str):
        self.patterns = patterns
        self.output = output

    def render(self, context):
        request_path = context['request'].path

        for pattern in self.patterns:
            pattern_path = template.Variable(pattern).resolve(context)

            if request_path.startswith(pattern_path):
                return self.output

        return ""


@register.tag
def if_current(parser, token):
    argv = token.split_contents()
    argc = len(argv)

    if argc < 3:
        raise template.TemplateSyntaxError(
            "%r tag requires at least three arguments, %d provided." % argv[0], argc)

    return isCurrentNode(argv[1:argc - 1], argv[-1])


@register.filter
def values_list(queryset, key):
    return queryset[:3].values_list(key, flat=True)
