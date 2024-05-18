from django.contrib import admin
from django.urls import path
from . import views

app_name = "fin_products"
urlpatterns = [
    path('financial_products/', views.financial_products),
    
    # 예금
    path('deposit/<fin_prdt_cd>/', views.deposit_detail),                                    # 단일 예금 상품 조회
    path('deposit/<fin_prdt_cd>/option_list/', views.depositoption_list),                    # 단일 예금 상품 옵션 목록 조회
    path('deposit/<fin_prdt_cd>/option_list/<option_pk>/', views.depositoption_detail),  # 단일 예금 상품 옵션 조회
    
    path('deposit/bank/all_bank/', views.deposit_list),                            # 전체 예금 목록 조회
    path('deposit/bank/<kor_co_nm>/', views.get_bank_deposits),                    # 금융기관별 예금상품 조회
    
    path('deposit/bank/all_bank/sort/<save_trm>/', views.get_all_deposits),        # 전체 금융기관에서 기간 선택 시 금리 내림차순 정렬
    path('deposit/bank/<kor_co_nm>/sort/<save_trm>/', views.get_reverse_deposits), # 금융기관별 기간 선택 시 금리 내림차순 정렬

    # 적금
    path('saving/<fin_prdt_cd>/', views.saving_detail),                                      # 단일 적금상품 조회
    path('saving/<fin_prdt_cd>/option_list/', views.savingoption_list),                      # 단일 적금상품 옵션 목록 조회   
    path('saving/<fin_prdt_cd>/option_list/<option_pk>/', views.savingoption_detail),    # 단일 적금상품 옵션 조회
    
    path('saving/all_bank/all_type/', views.saving_list),                        # 전체 적금 목록 조회
    path('saving/all_bank/<rsrv_type_nm>/', views.get_all_bank_savings),         # 전체 금융기관에서 적금유형별 조회
    path('saving/<kor_co_nm>/all_type/', views.get_bank_all_type_savings),       # 전체 적금유형에서 금융기관별 조회
    path('saving/<kor_co_nm>/<rsrv_type_nm>/', views.get_bank_type_savings),     # 적금유형별, 금융기관별 조회
    
    path('saving/all_bank/all_type/sort/<save_trm>/', views.get_all_bank_all_type_reverse_savings),        # 전체 금융기관, 전체 적금유형에서 기간 선택 시 금리 내림차순 정렬
    path('saving/all_bank/<rsrv_type_nm>/sort/<save_trm>/', views.get_all_bank_type_reverse_savings),       # 전체 금융기관에서 특정 적금유형과 기간 선택 시 금리 내림차순 정렬
    path('saving/<kor_co_nm>/all_type/sort/<save_trm>/', views.get_bank_all_type_reverse_savings),     # 전체 적금유형에서 특정 금융기관과 기간 선택 시 금리 내림차순 정렬
    path('saving/<kor_co_nm>/<rsrv_type_nm>/sort/<save_trm>/', views.get_bank_type_reverse_savings),   # 특정 금융기관, 특정 적금유형, 기간 선택 시 금리 내림차순 정렬
    
    # 대출
    path('loan/<fin_prdt_cd>/', views.loan_detail),                                          # 단일 대출상품 조회
    path('loan/<fin_prdt_cd>/option_list/', views.loanoption_list),                          # 단일 대출상품 옵션 목록 조회
    path('loan/<fin_prdt_cd>/option_list/<option_pk>/', views.loanoption_detail),        # 단일 대출상품 옵션 조회   

    path('loan/all_bank/all_type/', views.loan_list),                      # 전체 대출 목록 조회
    path('loan/all_bank/<mrtg_type>/', views.get_all_bank_type_loans),     # 전체 금융기관에서 담보유형별 조회
    path('loan/<kor_co_nm>/all_type/', views.get_bank_all_type_loans),     # 전체 담보유형에서 금융기관별 조회
    path('loan/<kor_co_nm>/<mrtg_type>/', views.get_bank_type_loans),      # 담보유형별, 금융기관별 조회
    
    path('loan/all_bank/all_type/sort/min_rate/', views.get_all_bank_all_type_min_loans),    # 전체 금융기관에서 대출금리 오름차순(min)       
    path('loan/all_bank/all_type/sort/max_rate/', views.get_all_bank_all_type_max_loans),    # 전체 금융기관에서 대출금리 오름차순(max)      
    path('loan/all_bank/all_type/sort/avg_rate/', views.get_all_bank_all_type_avg_loans),    # 전체 금융기관에서 대출금리 오름차순(avg)       
    path('loan/all_bank/<mrtg_type>/sort/min_rate/', views.get_all_bank_type_min_loans),     # 전체 금융기관에서 담보유형별 대출금리 오름차순(min)
    path('loan/all_bank/<mrtg_type>/sort/max_rate/', views.get_all_bank_type_max_loans),     # 전체 금융기관에서 담보유형별 대출금리 오름차순(max)
    path('loan/all_bank/<mrtg_type>/sort/avg_rate/', views.get_all_bank_type_avg_loans),     # 전체 금융기관에서 담보유형별 대출금리 오름차순(avg)
    path('loan/<kor_co_nm>/<mrtg_type>/sort/min_rate/', views.get_bank_type_min_loans),      # 전체 담보유형에서 금융기관별 대출금리 오름차순(min)          
    path('loan/<kor_co_nm>/<mrtg_type>/sort/max_rate/', views.get_bank_type_max_loans),      # 전체 담보유형에서 금융기관별 대출금리 오름차순(max)          
    path('loan/<kor_co_nm>/<mrtg_type>/sort/avg_rate/', views.get_bank_type_avg_loans),      # 전체 담보유형에서 금융기관별 대출금리 오름차순(avg)          
    
    # 상품 가입/취소 + 조회
    path('deposit/contract/<fin_prdt_cd>/', views.deposit_contract),   # 예금 
    path('saving/contract/<fin_prdt_cd>/', views.saving_contract),     # 적금 
    path('loan/contract/<fin_prdt_cd>/', views.loan_contract),         # 대출
    # 관심상품 저장/취소 + 조회
    path('deposit/like/<fin_prdt_cd>/', views.deposit_like),           # 예금 
    path('saving/like/<fin_prdt_cd>/', views.saving_like),             # 적금 
    path('loan/like/<fin_prdt_cd>/', views.loan_like),                 # 대출 

    ]
