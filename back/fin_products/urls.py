from django.contrib import admin
from django.urls import path
from . import views

app_name = "fin_products"
urlpatterns = [
    path('financial_products/', views.financial_products),
    path('deposit/', views.deposit_list),
    path('deposit/<code>/', views.deposit_detail),
    path('deposit/<code>/option_list/', views.depositoption_list),
    path('deposit/<code>/option_list/<int:option_pk>/', views.depositoption_detail),
    path('saving/', views.saving_list),
    path('saving/<code>/', views.saving_detail),
    path('saving/<code>/option_list/', views.savingoption_list),
    path('saving/<code>/option_list/<int:option_pk>/', views.savingoption_detail),
    path('loan/', views.loan_list),
    path('loan/<code>/', views.loan_detail),
    path('loan/<code>/option_list/', views.loanoption_list),
    path('loan/<code>/option_list/<int:option_pk>/', views.loanoption_detail),
    path('deposit/aes_sort/<int:save_trm>/', views.get_deposits),
    path('deposit/des_sort/<int:save_trm>/', views.get_reverse_deposits),
    path('saving/aes_sort/<int:save_trm>/', views.get_savings),
    path('saving/des_sort/<int:save_trm>/', views.get_reverse_savings),
    path('loan/min_aes_sort/<mrtg_type>/', views.get_min_loans),
    path('loan/min_des_sort/<mrtg_type>/', views.get_reverse_min_loans),
    path('loan/max_aes_sort/<mrtg_type>/', views.get_max_loans),
    path('loan/max_des_sort/<mrtg_type>/', views.get_reverse_max_loans),
    path('loan/avg_aes_sort/<mrtg_type>/', views.get_avg_loans),
    path('loan/avg_des_sort/<mrtg_type>/', views.get_reverse_avg_loans),
    path('bank_deposit/<kor_co_nm>/', views.bank_deposit),
    path('bank_saving/<kor_co_nm>/', views.bank_saving),
    path('bank_loan/<kor_co_nm>/', views.bank_loan), 
    path('contract_deposit/<code>/', views.contract_deposit),
    path('contract_saving/<code>/', views.contract_saving),
    path('contract_loan/<code>/', views.contract_loan),

    ]
