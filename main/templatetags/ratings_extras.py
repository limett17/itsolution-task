from django import template

register = template.Library()


@register.filter
def get_rating(ratings_dict, quote_id):
    return ratings_dict.get(quote_id)
