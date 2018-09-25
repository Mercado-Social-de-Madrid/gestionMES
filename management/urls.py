
from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^users/$', views.UsersListView.as_view(), name='users_list'),

]


