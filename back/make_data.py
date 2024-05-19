# make_data.py 파일은 랜덤한 더미 데이터를 만드는 예시 파일입니다.
# 반드시, 사용하는 필드를 확인한 후 본인의 프로젝트에 맞게 수정하여 진행해야 합니다.

# [참고] 현재 코드는 아래 User 모델을 기준으로 작성되어 있습니다.
"""
SAVING_PROPENSITY_CHOICES = [
        ('알뜰형', '알뜰형'),
        ('도전형', '도전형'),
        ('성실형', '성실형'),
    ]

    email = models.EmailField(max_length=300, blank=True, null=True)                                     # 이메일
    age = models.IntegerField()                                                                          # 나이
    profile_img = models.ImageField(upload_to='image/', default='image/user.png')                        # 프로필 이미지
    nickname = models.CharField(max_length=50)                                                           # 닉네임(ID)
    annual_income = models.IntegerField(blank=True, null=True)                                           # 연봉
    property = models.IntegerField(blank=True, null=True)                                                # 자산  
    main_bank = models.CharField(max_length=50, blank=True, null=True)                                   # 주거래 은행
    saving_propensity = models.CharField(max_length=20, choices=SAVING_PROPENSITY_CHOICES)               # 성향
"""


import random
import requests

first_name_samples = '김이박최정강조윤장임고장채지황허'
middle_name_samples = '민서예지도하주윤채현지기보정정'
last_name_samples = '준윤우원호후서연아은진수영람민욱'


def random_name():
    result = ''
    result += random.choice(first_name_samples)
    result += random.choice(middle_name_samples)
    result += random.choice(last_name_samples)
    return result + str(random.randint(1, 100))


# 현재 API 에 들어있는 금융 상품 코드 리스트 저장
DP_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
SP_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
LP_URL = 'http://finlife.fss.or.kr/finlifeapi/mortgageLoanProductsSearch.json'

API_KEY = 'f85e8d0bb15539c70a663845720483dc'

financial_products1 = []
financial_products2 = []
financial_products3 = []

params = {
    'auth': API_KEY,
    # 금융회사 코드 020000(은행), 030200(여신전문), 030300(저축은행), 050000(보험), 060000(금융투자)
    'topFinGrpNo': '020000',
    'pageNo': 1,
}

# 정기예금 목록 저장
response1 = requests.get(DP_URL, params=params).json()
baseList1 = response1.get('result').get('baseList')  # 상품 목록
# 적금 목록 저장
response2 = requests.get(SP_URL, params=params).json()
baseList2 = response2.get('result').get('baseList')  # 상품 목록
# 주택담보대출 목록 저장
response3 = requests.get(LP_URL, params=params).json()
baseList3 = response3.get('result').get('baseList')  # 상품 목록


for product1 in baseList1:
    financial_products1.append(product1['fin_prdt_cd'])
for product2 in baseList2:
    financial_products2.append(product2['fin_prdt_cd'])
for product3 in baseList3:
    financial_products3.append(product3['fin_prdt_cd'])


dict_keys = [
    'username',
    'age',
    'annual_income',
    'property',
]

# json 파일 만들기
import json
from collections import OrderedDict

file = OrderedDict()

username_list = []
N = 100000
i = 0

while i < N:
    rn = random_name()
    if rn in username_list:
        continue

    username_list.append(rn)
    i += 1


# 저장 위치는 프로젝트 구조에 맞게 수정합니다.
save_dir = './accounts/fixtures/accounts/user_data.json'
with open(save_dir, 'w', encoding="utf-8") as f:
    f.write('[')

    for i in range(N):
        # 랜덤한 데이터를 삽입
        file['model'] = 'accounts.User'
        file['pk'] = i + 1
        file['fields'] = {
            'username': username_list[i],  # 유저 이름 랜덤 생성
            # 랜덤한 0~5개의 상품을 가입하도록 삽입됨
            'D_products': ','.join(
                [
                    random.choice(financial_products1)
                    for _ in range(random.randint(0, 5))
                ]
            ),  # 금융 상품 리스트
            'S_products': ','.join(
                [
                    random.choice(financial_products2)
                    for _ in range(random.randint(0, 5))
                ]
            ),  # 금융 상품 리스트
            'L_products': ','.join(
                [
                    random.choice(financial_products3)
                    for _ in range(random.randint(0, 5))
                ]
            ),  # 금융 상품 리스트
            'age': random.randint(1, 100),  # 나이
            'annual_income': random.randrange(0, 100000000, 100000),  # 현재 가진 금액
            'property': random.randrange(0, 1500000000, 1000000),  # 연봉
            'password': '1234',
            'nickname': None,
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }
   
        json.dump(file, f, ensure_ascii=False, indent='\t')
        if i != N - 1:
            f.write(',')
    f.write(']')
    f.close()

print(f'데이터 생성 완료 / 저장 위치: {save_dir}')
