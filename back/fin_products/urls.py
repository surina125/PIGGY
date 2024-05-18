from django.contrib import admin
from django.urls import path
from . import views

app_name = "fin_products"
urlpatterns = [
    path('financial_products/', views.financial_products),
    path('deposit/', views.deposit_list),                                                                           # 전체 예금 목록 조회
    path('deposit/<code>/', views.deposit_detail),                                                                  # 단일 예금 상품 조회
    path('deposit/<code>/option_list/', views.depositoption_list),                                                  # 단일 예금 상품 옵션 목록 조회
    path('deposit/<code>/option_list/<int:option_pk>/', views.depositoption_detail),                                # 단일 예금 상품 옵션 조회
    path('saving/', views.saving_list),                                                                             # 전체 적금 목록 조회
    path('saving/<code>/', views.saving_detail),                                                                    # 단일 적금상품 조회
    path('saving/<code>/option_list/', views.savingoption_list),                                                    # 단일 적금상품 옵션 목록 조회   
    path('saving/<code>/option_list/<int:option_pk>/', views.savingoption_detail),                                  # 단일 적금상품 옵션 조회
    path('loan/', views.loan_list),                                                                                 # 전체 대출 목록 조회
    path('loan/<code>/', views.loan_detail),                                                                        # 단일 대출상품 조회
    path('loan/<code>/option_list/', views.loanoption_list),                                                        # 단일 대출상품 옵션 목록 조회
    path('loan/<code>/option_list/<int:option_pk>/', views.loanoption_detail),                                      # 단일 대출상품 옵션 조회   

    # path('deposit/des_sort/all/', views.get_all_deposits),                         >> deposit_list와 동일                               # 전체 금융기관 예금상품
    path('deposit/all_bank/<kor_co_nm>/', views.get_bank_deposits),                                                 # 금융기관별 예금상품
    path('deposit/des_sort/<kor_co_nm>/<int:save_trm>/', views.get_reverse_deposits),                               # 금융기관별 예금 금리 내림차순


    # path('saving/des_sort/all_type/all_bank/', views.get_all_bank_savings),          >> saving_list와 동일                              # 전체 금융기관 적금
    path('saving/all_bank/<rsrv_type_nm>/', views.get_all_bank_all_type_savings),                                   # 전체 금융기관 적금(적금유형별)
    path('saving/<kor_co_nm>/all_type/', views.get_bank_all_type_savings),                                          # 금융기관별 적금 
    path('saving/<kor_co_nm>/<rsrv_type_nm>/', views.get_bank_type_savings),                                        # 금융기관별 적금(적금유형별)
    path('saving/des_sort/all_type/all_bank/<int:save_trm>/', views.get_all_bank_reverse_savings),                  # 전체 금융기관 적금 금리 내림차순(예치기간별)
    path('saving/des_sort/<rsrv_type_nm>/all_bank/<int:save_trm>/', views.get_all_bank_type_reverse_savings),       # 전체 금융기관 적금 금리 내림차순(적금유형별, 예치기간별)
    path('saving/des_sort/all_type/<kor_co_nm>/<int:save_trm>/', views.get_bank_all_type_reverse_savings),          # 금융기관별 적금 금리 내림차순(예치기간별)
    path('saving/des_sort/<rsrv_type_nm>/<kor_co_nm>/<int:save_trm>/', views.get_bank_type_reverse_savings),        # 금융기관별 적금 금리 내림차순(적금유형별, 예치기간 별)

    # path('loan/aes_sort/all_type/all_bank/', views.get_all_bank_loans),   >> loan_list와 동일                                        # 전체 금융기관 대출상품
    path('loan/all_bank/<mrtg_type>/', views.get_all_bank_type_loans),                                               # 전체 금융기관 대출상품(담보유형별)
    path('loan/<kor_co_nm>/all_type/', views.get_bank_all_type_loans),                                               # 금융기관 별 대출상품
    path('loan/<kor_co_nm>/<mrtg_type>/', views.get_bank_type_loans),                                                # 금융기관 별 대출(담보유형별)
    path('loan/aes_sort/all_bank/all_type/min_rate/', views.get_all_bank_all_type_min_loans),                        # 전체 금융기관 대출 금리 오름차순(min)       
    path('loan/aes_sort/all_bank/all_type/max_rate/', views.get_all_bank_all_type_max_loans),                        # 전체 금융기관 대출 금리 오름차순(max)      
    path('loan/aes_sort/all_bank/all_type/avg_rate/', views.get_all_bank_all_type_avg_loans),                        # 전체 금융기관 대출 금리 오름차순(avg)       
    path('loan/aes_sort/all_bank/type/min_rate/', views.get_all_bank_type_min_loans),                                # 전체 금융기관 대출 금리 오름차순(담보유형별, min)
    path('loan/aes_sort/all_bank/type/max_rate/', views.get_all_bank_type_max_loans),                                # 전체 금융기관 대출 금리 오름차순(담보유형별, max)
    path('loan/aes_sort/all_bank/type/avg_rate/', views.get_all_bank_type_avg_loans),                                # 전체 금융기관 대출 금리 오름차순(담보유형별, avg)
    path('loan/aes_sort/<kor_co_nm>/<mrtg_type>/min_rate/', views.get_bank_type_min_loans),                          # 금융기관 별 대출금리 오름차순(담보유형별, min)          
    path('loan/aes_sort/<kor_co_nm>/<mrtg_type>/max_rate/', views.get_bank_type_max_loans),                          # 금융기관 별 대출금리 오름차순(담보유형별, max)          
    path('loan/aes_sort/<kor_co_nm>/<mrtg_type>/avg_rate/', views.get_bank_type_avg_loans),                          # 금융기관 별 대출금리 오름차순(담보유형별, avg)          
    
    
    # path('deposit/bank/<kor_co_nm>/', views.deposit_bank),         >> get_bank_deposits와 동일                                       # 금융기관 별 예금상품
    # path('saving/bank/<kor_co_nm>/', views.saving_bank),           >> get_all_bank_all_type_savings와 동일                           # 금융기관 별 적금상품
    # path('loan/bank/<kor_co_nm>/', views.loan_bank),               >>  get_all_bank_all_type_loans와 동일                            # 금융기관 별 대출상품
    path('deposit_contract/<code>/', views.deposit_contract),                                                          # 예금 가입 및 가입한 예금 조회
    path('saving_contract/<code>/', views.saving_contract),                                                            # 적금 가입 및 가입한 적금 조회
    path('loan_contract/<code>/', views.loan_contract),                                                                # 대출 가입 및 가입한 대출 조회
    path('deposit_like/<code>/', views.deposit_like),                                                                  # 예금 가입 및 가입한 예금 조회
    path('saving_like/<code>/', views.saving_like),                                                                    # 적금 가입 및 가입한 적금 조회
    path('loan_like/<code>/', views.loan_like),                                                                        # 대출 가입 및 가입한 대출 조회

    ]
