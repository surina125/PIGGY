from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings


class Deposit(models.Model):
    dcls_month = models.CharField(max_length=20)                                                        # 공시제출월
    fin_co_no = models.CharField(max_length=100)                                                        # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)                                                        # 금융회사명
    fin_prdt_cd = models.CharField(max_length=100)                                                      # 금융상품코드
    fin_prdt_nm = models.CharField(max_length=100)                                                      # 금융상품명
    join_way = models.CharField(max_length=100)                                                         # 가입방법
    mtrt_int = models.TextField(blank=True, null=True)                                                  # 만기 후 이자율
    spcl_cnd = models.TextField(blank=True, null=True)                                                  # 우대조건
    join_deny = models.IntegerField(blank=True, null=True)                                              # 가입제한(1:제한없음, 2:서민전용, 3.일부제한)
    join_member = models.TextField(blank=True, null=True)                                               # 가입대상
    etc_note = models.TextField(blank=True, null=True)                                                  # 기타 유의사항
    max_limit = models.IntegerField(blank=True, null=True)                                              # 최고한도
    contract_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contract_deposit')   # 예금 상품 가입자
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_deposit')           # 예금 상품 좋아요 유저

class DepositOption(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)                                      # 금융상품코드
    intr_rate_type_nm = models.CharField(max_length=2)                                                  # 저축금리유형명        
    save_trm = models.CharField(max_length=3)                                                           # 저축기간[단위:개월]
    intr_rate = models.FloatField(null=True)                                                            # 저축금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True)                                                           # 최고 우대금리[소수점 2자리]



class Saving(models.Model):
    dcls_month = models.CharField(max_length=20)                                                        # 공시 제출월
    fin_co_no = models.CharField(max_length=100)                                                        # 금융회사코드
    kor_co_nm = models.CharField(max_length=100)                                                        # 금융회사명
    fin_prdt_cd = models.CharField(max_length=100)                                                      # 금융상품코드
    fin_prdt_nm = models.CharField(max_length=100)                                                      # 금융상품명
    join_way = models.CharField(max_length=100)                                                         # 가입방법
    mtrt_int = models.TextField(blank=True, null=True)                                                  # 만기 후 이자율
    spcl_cnd = models.TextField(blank=True, null=True)                                                  # 우대조건
    join_deny = models.IntegerField(blank=True, null=True)                                              # 가입제한(1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField(blank=True, null=True)                                               # 가입대상
    etc_note = models.TextField(blank=True, null=True)                                                  # 기타유의사항
    max_limit = models.IntegerField(blank=True, null=True)                                              # 최고한도
    contract_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contract_saving')    # 적금 상품 가입자
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_saving')            # 적금 상품 좋아요 유저

class SavingOption(models.Model):
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE)                                        # 금융상품코드
    intr_rate_type = models.CharField(max_length=2)                                                     # 저축금리유형
    intr_rate_type_nm = models.CharField(max_length=10)                                                 # 저축금리유형명
    rsrv_type_nm = models.CharField(max_length=10)                                                      # 적립유형명
    save_trm = models.CharField(max_length=3)                                                           # 저축기간[단위:개월]
    intr_rate = models.FloatField(null=True)                                                            # 저축금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True)                                                           # 최고 우대금리[소수점 2자리]



class Loan(models.Model):
    dcls_month = models.CharField(max_length=20)                                                        # 공시 제출월
    fin_co_no = models.CharField(max_length=100)                                                        # 금융회사코드
    kor_co_nm = models.CharField(max_length=100, blank=True)                                            # 금융회사명
    fin_prdt_cd = models.CharField(max_length=100)                                                      # 금융상품코드
    fin_prdt_nm = models.CharField(max_length=100)                                                      # 금융상품명
    join_way = models.CharField(max_length=100)                                                         # 가입방법
    erly_rpay_fee = models.TextField()                                                                  # 중도상환수수료
    dly_rate = models.TextField()                                                                       # 연체 이자율
    loan_lmt = models.TextField()                                                                       # 대출한도
    contract_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contract_loan')      # 대출 상품 가입자
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_loan')              # 대출 상품 좋아요 유저


class LoanOption(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)                                            # 금융상품코드
    mrtg_type = models.CharField(max_length=20, blank=True)                                             # 담보유형코드
    mrtg_type_nm = models.CharField(max_length=20, blank=True)                                          # 담보유형
    rpay_type_nm = models.CharField(max_length=20)                                                      # 대출상환유형
    lend_rate_type_nm = models.CharField(max_length=20)                                                 # 대출금리유형
    lend_rate_min = models.FloatField(null=True)                                                        # 대출금리_최저[소수점 2자리]
    lend_rate_max = models.FloatField(null=True)                                                        # 대출금리_최고 [소수점 2자리]
    lend_rate_avg = models.FloatField(null=True)                                                        # 전월 취급 평균금리 [소수점 2자리]
                                                     
