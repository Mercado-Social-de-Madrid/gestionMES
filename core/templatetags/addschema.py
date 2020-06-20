import re
from django import template

register = template.Library()

@register.filter
def addschema(url):
    '''
    Prepends the http schema definition if the URL passed doesn't include it
    :param url: string containing a url
    :return:
    '''
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url