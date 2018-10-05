import itertools

from django import template

register = template.Library()

@register.filter
def chunks(value, chunk_length):
    """
    Breaks a list up into a list of lists of size <chunk_length>
    """
    clen = int(chunk_length)
    i = iter(value)
    while True:
        chunk = list(itertools.islice(i, clen))
        if chunk:
            yield chunk
        else:
            break


@register.filter
def split(value, arg):
    """
    Splits a string into an array by the argument
    """
    return value.split(arg)