from django.db import models

# Create your models here.

class Exchange (models.Model):
    CUR_UNIT = models.CharField(max_length=100)        # 통화코드
    CUR_NM = models.CharField(max_length=100)          # 국가/통화명
    TTB = models.CharField(max_length=100)             # 전신환(송금) 받으실 때
    TTS = models.CharField(max_length=100)             # 전신환(송금) 보내실 떄
    DEAL_BAS_R = models.CharField(max_length=100)      # 매매 기준율
    BKPR = models.CharField(max_length=100)            # 장부가격
    YY_EFEE_R = models.CharField(max_length=100)       # 년환가료율
    TEN_DD_EFEE_R = models.CharField(max_length=100)   # 10일환가료율
    KFTC_DEAL_BAS_R = models.CharField(max_length=100) # 서울외국환중개 매매기준율
    KFTC_BKPR = models.CharField(max_length=100)       # 서울외국환중개 장부가격
    