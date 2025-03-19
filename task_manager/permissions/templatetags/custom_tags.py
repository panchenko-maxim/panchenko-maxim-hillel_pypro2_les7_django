from django import template

register = template.Library()

@register.simple_tag
def multiply(x, y):
    return x * y

@register.tag(name='uppercasecustom')
def do_uppercase(parser, token):
    nodelist = parser.parse(('enduppercase',))
    parser.delete_first_token()
    return UppercaseNode(nodelist)

class UppercaseNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        return content.upper()

@register.filter(name='format_number')
def format_number(value):
    return f"{value:,}".replace(',', ' ')

@register.filter(name='in_list')
def in_list(value, arg):
    return value in arg