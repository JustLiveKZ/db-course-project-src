from django import template

register = template.Library()


@register.filter()
def bootstrap_class(tags):
    return 'danger' if tags == 'error' else tags


@register.assignment_tag()
def get_contextual_bg(required_quantity, available_quantity):
    if required_quantity <= available_quantity:
        return 'success'
    else:
        return 'danger'