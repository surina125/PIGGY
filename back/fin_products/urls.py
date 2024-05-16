from django.contrib import admin
from django.urls import path
from . import views

app_name = "fin_products"
urlpatterns = [
    path('financial_products/', views.financial_products),
    path('deposit_list/', views.deposit_list),
    path('deposit_list/<code>/', views.deposit_detail),
    path('deposit_list/<code>/option_list/', views.depositoption_list),
    path('deposit_list/<code>/option_list/<int:option_pk>/', views.depositoption_detail),
    path('saving_list/', views.saving_list),
    path('saving_list/<code>/', views.saving_detail),
    path('saving_list/<code>/option_list/', views.savingoption_list),
    path('saving_list/<code>/option_list/<int:option_pk>/', views.savingoption_detail),
    path('loan_list/', views.loan_list),
    path('loan_list/<code>/', views.loan_detail),
    path('loan_list/<code>/option_list/', views.loanoption_list),
    path('loan_list/<code>/option_list/<int:option_pk>/', views.loanoption_detail),
    path('deposit/aes_sort/<int:save_trm>', views.get_deposits),
    path('deposit/des_sort/<int:save_trm>', views.get_reverse_deposits),
    path('saving/aes_sort/<int:save_trm>', views.get_savings),
    path('saving/des_sort/<int:save_trm>', views.get_reverse_savings),
    
    path('loan/min_aes_sort/<mrtg_type>/', views.get_min_loans),
    # path('loan/min_rate_E/', views.get_min_loans,{'mrtg_type':'E'}),
    path('loan/min_des_sort/<type>/', views.get_reverse_min_loans),
    # path('loan/min_rate_reverse_E/', views.get_reverse_min_loans, {'mrtg_type':'E'}),

    path('loan/max_aes_sort/<mrtg_type>/', views.get_max_loans),
    # path('loan/max_rate_E/', views.get_max_loans,{'mrtg_type':'E'}),
    path('loan/max_des_sort/<type>/', views.get_reverse_max_loans),
    # path('loan/max_rate_reverse_E/', views.get_reverse_max_loans, {'mrtg_type':'E'}),

    path('loan/avg_aes_sort/<mrtg_type>/', views.get_avg_loans),
    # path('loan/avg_rate_E/', views.get_avg_loans,{'mrtg_type':'E'}),
    path('loan/avg_des_sort/<type>/', views.get_reverse_avg_loans),
    # path('loan/avg_rate_reverse_E/', views.get_reverse_avg_loans, {'mrtg_type':'E'}),

    path('bank_deposit/<kor_co_nm>/', views.bank_deposit),
    path('bank_saving/<kor_co_nm>/', views.bank_saving),
    path('bank_loan/<kor_co_nm>/', views.bank_loan),

]


    # path('deposit/12/', views.get_deposits, {'save_trm': '12'}),
    # path('deposit/24/', views.get_deposits, {'save_trm': '24'}),
    # path('deposit/36/', views.get_deposits, {'save_trm': '36'}),
    # path('deposit/12_reverse/', views.get_reverse_deposits, {'save_trm': '12'}),
    # path('deposit/24_reverse/', views.get_reverse_deposits, {'save_trm': '24'}),
    # path('deposit/36_reverse/', views.get_reverse_deposits, {'save_trm': '36'}),
    # path('saving/12/', views.get_savings, {'save_trm': '12'}),
    # path('saving/24/', views.get_savings, {'save_trm': '24'}),
    # path('saving/36/', views.get_savings, {'save_trm': '36'}),
    # path('saving/12_reverse/', views.get_reverse_savings, {'save_trm': '12'}),
    # path('saving/24_reverse/', views.get_reverse_savings, {'save_trm': '24'}),
    # path('saving/36_reverse/', views.get_reverse_savings, {'save_trm': '36'}),