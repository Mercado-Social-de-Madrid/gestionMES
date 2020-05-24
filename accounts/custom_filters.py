# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator

import django_filters
from django.db.models import Q

from accounts.models import Account
from core.filters.SearchFilter import SearchFilter


class AccountSearchFilter(SearchFilter):
    def __init__(self,names,*args,**kwargs):
        if len(args) == 0:
            kwargs['field_name'] = names[0]
        self.token_prefix = kwargs.pop('token_prefix','')
        self.token_suffix = kwargs.pop('token_suffix','')
        self.token_reducer = kwargs.pop('token_reducer',operator.and_)
        self.names = names
        django_filters.Filter.__init__(self,*args,**kwargs)


    def get_subquery_list(self, search_value):

        queries = super().get_subquery_list(search_value)
        accounts = Account.objects.filter(
            Q(Consumer___first_name__icontains=search_value) | Q(Consumer___last_name__icontains=search_value) |
            Q(Entity___name__icontains=search_value) | Q(Entity___business_name__icontains=search_value)
        )
        print(accounts.count())
        queries.append(Q(account__in=accounts))
        return queries
