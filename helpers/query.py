import re

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.db.models import Q
import datetime


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):

    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''

    return [normspace('', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):

    '''
    Returns a query, that is a combination of Q objects.
    That combination aims to search keywords within a model by testing the given search fields.
    '''

    query = None  # Query to search for every search term
    terms = normalize_query(query_string)

    for term in terms:
        if len(term)<3:
            continue
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query

    return query


def paginate(list, page, elems_perpage=10):
    paginator = Paginator(list, elems_perpage)
    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated = paginator.page(1)
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated = paginator.page(paginator.num_pages)

    return paginated


def generate_graph_data(stats_bydate, is_monthly=False):
    dates = []

    current_date = None
    current_stats = {}

    for date in stats_bydate:
        if is_monthly:
            #depending if it is monthly or daily, we parse differently the day "tag"
            day = datetime.date(month=date['month'], year=date['year'], day=1)
        else:
            day = date['day']

        if current_date is None or day != current_date:
            if current_date != None:
                dates.append([current_date, current_stats])
            current_date = day
            current_stats = {'total':0}

        current_stats['bonus' if date['is_bonification'] else 'normal'] = date['total']
        current_stats['total'] += date['total']

    if current_date is not None:
        dates.append([current_date, current_stats])

    return dates