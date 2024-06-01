from django.contrib import admin
from django.urls import path
from . import views

app_name = "fin_products"
urlpatterns = [
    path('financial_products/', views.financial_products),
 
    path('recommend_two/', views.recommend_two, name='recommend_two'), # 추천
 
    # 예금
    path('deposit/<fin_prdt_cd>/', views.deposit_detail),                                    # 단일 예금 상품 조회

    path('deposit/bank/all_bank/', views.deposit_list),                            # 전체 예금 목록 조회
    path('deposit/bank/<kor_co_nm>/', views.get_bank_deposits),                    # 금융기관별 예금상품 조회
    
    path('deposit/bank/all_bank/sort/<save_trm>/', views.get_all_deposits),        # 전체 금융기관에서 기간 선택 시 금리 내림차순 정렬
    path('deposit/bank/<kor_co_nm>/sort/<save_trm>/', views.get_reverse_deposits), # 금융기관별 기간 선택 시 금리 내림차순 정렬

    # 적금
    path('savings/<fin_prdt_cd>/', views.saving_detail),                                      # 단일 적금상품 조회

    path('savings/all_bank/all_type/', views.saving_list),                        # 전체 적금 목록 조회
    path('savings/all_bank/<rsrv_type_nm>/', views.get_all_bank_savings),         # 전체 금융기관에서 적금유형별 조회
    path('savings/<kor_co_nm>/all_type/', views.get_bank_all_type_savings),       # 전체 적금유형에서 금융기관별 조회
    path('savings/<kor_co_nm>/<rsrv_type_nm>/', views.get_bank_type_savings),     # 적금유형별, 금융기관별 조회
    
    path('savings/all_bank/all_type/sort/<save_trm>/', views.get_all_bank_all_type_reverse_savings),        # 전체 금융기관, 전체 적금유형에서 기간 선택 시 금리 내림차순 정렬
    path('savings/all_bank/<rsrv_type_nm>/sort/<save_trm>/', views.get_all_bank_type_reverse_savings),       # 전체 금융기관에서 특정 적금유형과 기간 선택 시 금리 내림차순 정렬
    path('savings/<kor_co_nm>/all_type/sort/<save_trm>/', views.get_bank_all_type_reverse_savings),     # 전체 적금유형에서 특정 금융기관과 기간 선택 시 금리 내림차순 정렬
    path('savings/<kor_co_nm>/<rsrv_type_nm>/sort/<save_trm>/', views.get_bank_type_reverse_savings),   # 특정 금융기관, 특정 적금유형, 기간 선택 시 금리 내림차순 정렬
    
    # 대출
    path('loans/<fin_prdt_cd>/', views.loan_detail),                                          # 단일 대출상품 조회

    path('loans/all_bank/all_type/', views.loan_list),                      # 전체 대출 목록 조회

    # 상품 가입/취소/조회 
    path('deposit/contract/<fin_prdt_cd>/', views.deposit_contract),   # 예금 
    path('saving/contract/<fin_prdt_cd>/', views.saving_contract),     # 적금 
    path('loan/contract/<fin_prdt_cd>/', views.loan_contract),         # 대출
   
   # 상품 가입 조회
    path('dep/contract/search/', views.deposit_contract_list),      # 예금 
    path('sav/contract/search/', views.saving_contract_list),        # 적금 
    path('loa/contract/search/', views.loan_contract_list),            # 대출 

    # 관심상품 저장/취소/조회
    path('deposit/like/<fin_prdt_cd>/', views.deposit_like),           # 예금 
    path('saving/like/<fin_prdt_cd>/', views.saving_like),             # 적금 
    path('loan/like/<fin_prdt_cd>/', views.loan_like),                 # 대출 

    # 관심상품 조회 조회
    path('dep/like/search/', views.deposit_like_list),             # 예금 
    path('sav/like/search/', views.saving_like_list),              # 적금 
    path('loa/like/search/', views.loan_like_list),                # 대출 

    ]
