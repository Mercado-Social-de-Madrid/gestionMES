from django.urls import path

from . import views


urlpatterns = [
    path('', view=views.sermepa_ipn, name='sermepa_ipn'),
    path('<pk>', views.SermepaResponseDetailView.as_view(), name='sermepa_response')
]
