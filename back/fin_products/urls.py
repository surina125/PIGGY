from django.contrib import admin
from django.urls import path
from . import views

app_name = "fin_products"
urlpatterns = [
    path('financial_products/', views.financial_products),
    path('deposit/', views.deposit_list),                                             # 전체 예금 목록 조회
    path('deposit/<code>/', views.deposit_detail),                                    # 단일 예금 상품 조회
    path('deposit/<code>/option_list/', views.depositoption_list),                    # 단일 예금 상품 옵션 목록 조회
    path('deposit/<code>/option_list/<int:option_pk>/', views.depositoption_detail),  # 단일 예금 상품 옵션 조회
    path('saving/', views.saving_list),                                               # 전체 적금 목록 조회
    path('saving/<code>/', views.saving_detail),                                      # 단일 적금상품 조회
    path('saving/<code>/option_list/', views.savingoption_list),                      # 단일 적금상품 옵션 목록 조회   
    path('saving/<code>/option_list/<int:option_pk>/', views.savingoption_detail),    # 단일 적금상품 옵션 조회
    path('loan/', views.loan_list),                                                   # 전체 대출 목록 조회
    path('loan/<code>/', views.loan_detail),                                          # 단일 대출상품 조회
    path('loan/<code>/option_list/', views.loanoption_list),                          # 단일 대출상품 옵션 목록 조회
    path('loan/<code>/option_list/<int:option_pk>/', views.loanoption_detail),        # 단일 대출상품 옵션 조회
    path('deposit/des_sort/all/<int:save_trm>/', views.get_all_reverse_deposits),     # 전체 금융기관 예금 금리 내림차순(예치기간 별)
    path('deposit/des_sort/<kor_co_nm>/<int:save_trm>/', views.get_reverse_deposits), # 금융기관 별 예금 금리 내림차순(예치기간 별)
    path('saving/des_sort/all/<int:save_trm>/', views.get_all_reverse_savings),       # 전체 금융기관 적금 금리 내림차순(예치기간 별)
    path('saving/des_sort/<kor_co_nm>/<int:save_trm>/', views.get_reverse_savings),   # 금융기관 별 적금 금리 내림차순(예치기간 별)
    # path('loan/aes_sort/all/<mrtg_type>/', views.get_aes_loans),                      # 전체 금융기관 대출 금리 내림차순(예치기간 별)
    path('loan/min_aes_sort/<kor_co_nm>/<mrtg_type>/', views.get_min_loans),          # 금융기관 별 최저 대출 금리 오름차순(담보유형)
    path('loan/max_aes_sort/<kor_co_nm>/<mrtg_type>/', views.get_max_loans),          # 금융기관 별 최대 대출 금리 오름차순(담보유형)
    path('loan/avg_aes_sort/<kor_co_nm>/<mrtg_type>/', views.get_avg_loans),          # 금융기관 별 평균 대출 금리 오름차순(담보유형)
    path('deposit/bank/<kor_co_nm>/', views.deposit_bank),                            # 금융기관 별 예금상품
    path('saving/bank/<kor_co_nm>/', views.saving_bank),                              # 금융기관 별 적금상품
    path('loan/bank/<kor_co_nm>/', views.loan_bank),                                  # 금융기관 별 대출상품
    path('deposit_contract/<code>/', views.deposit_contract),
    path('saving_contract/<code>/', views.saving_contract),
    path('loan_contract/<code>/', views.loan_contract),

    ]
