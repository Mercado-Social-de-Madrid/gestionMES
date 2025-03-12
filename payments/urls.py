
from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [

    path('', views.PaymentsListView.as_view(), name='payments_list'),
    path('create/', views.PaymentCreate.as_view(), name='create_payment'),
    path('year/<int:year>/', views.PaymentsListView.as_view(), name='list_by_year'),
    path('<pk>', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('<pk>/update/', views.update_payment, name='update_payment'),
    path('<pk>/delete/', views.payment_delete, name='payment_delete'),
    path('<pk>/fee/', views.assign_payment_to_annualfeecharge, name='assign_fee'),
    path('card/', views.CardPaymentsListView.as_view(), name='card_payments_list'),
    path('card/<pk>/', views.CardPaymentDetailView.as_view(), name='card_payment_detail'),
    path('pay/<uuid>/', views.form, name='payment_form'),
    path('end/success/', views.payment_success, name='payment_success'),
    path('end/error/', views.payment_error, name='payment_error'),

    path('<pk>/factura.pdf', views.invoice_pdf, name='invoice_pdf'),

    path('annual/<int:year>/', views.AnnualFeeChargesList.as_view(), name='annual_feecharges'),
    path('annual/<int:year>/fee/<int:pk>)', views.SplitFeeCharge.as_view(), name='split_feecharge'),

    path('sepa/', views.SepaBatchListView.as_view(), name='sepa_list'),
    path('sepa/add/', views.BatchCreate.as_view(), name='sepa_create'),
    path('sepa/update/<pk>/', views.BatchUpdate.as_view(), name='sepa_update'),
    path('sepa/<pk>/', views.BatchDetail.as_view(), name='sepa_detail'),
    path('sepa/<pk>/regenerate/', views.sepa_regenerate, name='sepa_regenerate'),
    path('sepa/<pk>/delete/', views.sepa_delete, name='sepa_delete'),
    path('sepa/<pk>/<batch_pk>/invoice', views.batch_payment_pdf, name='batch_payment_pdf'),
    path('sepa/<pk>/set-paid/', views.sepa_set_paid, name='sepa_set_paid'),

    path('banks/', views.BankList.as_view(), name='bank_list'),
    path('banks/bic', views.BicExplanation.as_view(), name='bic_explanation'),
    path('banks/add/', views.BankCreate.as_view(), name='bank_create'),
    path('banks/<pk>/', views.BankUpdate.as_view(), name='bank_detail'),

    path('fees/add_comment/', views.add_fee_comment, name='add_fee_comment'),
    path('fees/generate/', views.GenerateFeesView.as_view(), name='generate_fees'),
]

