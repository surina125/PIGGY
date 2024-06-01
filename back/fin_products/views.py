from collections import Counter
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import requests
from .serializers import *
from .models import *


@api_view(['POST', 'GET'])
def recommend_two(request, obj):
    if request.method == 'POST':
        data = request.data
        product = data.get('product')
        interest_rate = data.get('interestRate')
        period = data.get('period')
        banks = data.get('banks')
        # 필요에 따라 추가 데이터를 처리합니다
        return Response({'message': 'Data received', 'product': product, 'interestRate': interest_rate, 'period': period, 'banks': banks}, status=status.HTTP_200_OK)
        

# 금융상품 데이터 DB 저장
@api_view(['GET'])
def financial_products(request):

    DEPOSIT_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={settings.API_KEY}&topFinGrpNo=020000&pageNo=1'
    SAVING_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={settings.API_KEY}&topFinGrpNo=020000&pageNo=1'
    LOAN_API_URL = f'http://finlife.fss.or.kr/finlifeapi/mortgageLoanProductsSearch.json?auth={settings.API_KEY}&topFinGrpNo=050000&pageNo=1'
   

    deposit_info = requests.get(DEPOSIT_API_URL).json()
    deposit_baseList = deposit_info.get('result').get('baseList')
    deposit_optionList = deposit_info.get('result').get('optionList')

    for deposit_base in deposit_baseList:

        fin_prdt_cd = deposit_base.get('fin_prdt_cd')

        # 동일한 금융상품 존재한다면 DB에 추가하지 않음
        if Deposit.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue

        save_deposit = {
            'dcls_month': deposit_base.get('dcls_month'), 
            'fin_co_no': deposit_base.get('fin_co_no'), 
            'kor_co_nm': deposit_base.get('kor_co_nm'), 
            'fin_prdt_cd': deposit_base.get('fin_prdt_cd'), 
            'fin_prdt_nm': deposit_base.get('fin_prdt_nm'),
            'join_way': deposit_base.get('join_way'),
            'mtrt_int': deposit_base.get('mtrt_int'),
            'spcl_cnd': deposit_base.get('spcl_cnd'), 
            'join_deny': deposit_base.get('join_deny'), 
            'join_member': deposit_base.get('join_member'), 
            'etc_note': deposit_base.get('etc_note'), 
            'max_limit': deposit_base.get('max_limit') 
        }

        serializer = DepositSerializer(data=save_deposit)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for deposit_option in deposit_optionList:

        option_prdt_cd = deposit_option.get('fin_prdt_cd')
        product = Deposit.objects.get(fin_prdt_cd=option_prdt_cd)

        save_option = {
        'intr_rate_type_nm': deposit_option.get('intr_rate_type_nm'),
        'intr_rate': deposit_option.get('intr_rate'), 
        'intr_rate2': deposit_option.get('intr_rate2'), 
        'save_trm': deposit_option.get('save_trm'), 
        }

        serializer = DepositOptionSerializer(data=save_option)
        if serializer.is_valid(raise_exception=True):
            serializer.save(deposit=product)


    saving_info = requests.get(SAVING_API_URL).json()   
    saving_baseList = saving_info.get('result').get('baseList')
    saving_optionList = saving_info.get('result').get('optionList')

    for saving_base in saving_baseList:

        fin_prdt_cd = saving_base.get('fin_prdt_cd')

        # 동일한 금융상품 존재한다면 DB에 추가하지 않음
        if Saving.objects.filter(fin_prdt_cd = fin_prdt_cd).exists():
            continue

        save_product = {
            'dcls_month': saving_base.get('dcls_month'),
            'fin_co_no': saving_base.get('fin_co_no'),
            'kor_co_nm': saving_base.get('kor_co_nm'),
            'fin_prdt_cd': saving_base.get('fin_prdt_cd'),
            'fin_prdt_nm': saving_base.get('fin_prdt_nm'),
            'join_way': saving_base.get('join_way'),
            'mtrt_int': saving_base.get('mtrt_int'),
            'spcl_cnd': saving_base.get('spcl_cnd'),
            'join_deny': saving_base.get('join_deny'),
            'join_member': saving_base.get('join_member'),
            'etc_note': saving_base.get('etc_note'),
            'max_limit': saving_base.get('max_limit'),
        }
        serializer = SavingSerializer(data=save_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for save_option in saving_optionList:
        option_prdt_cd = save_option.get('fin_prdt_cd')
        product = Saving.objects.get(fin_prdt_cd=option_prdt_cd)
        save_option = {
            'intr_rate_type': save_option.get('intr_rate_type'),
            'intr_rate_type_nm': save_option.get('intr_rate_type_nm'),
            'rsrv_type_nm' : save_option.get('rsrv_type_nm'),
            'intr_rate': save_option.get('intr_rate'),
            'intr_rate2': save_option.get('intr_rate2'),
            'save_trm': save_option.get('save_trm'),
        }

        serializer = SavingOptionSerializer(data=save_option)
        if serializer.is_valid(raise_exception=True):
            serializer.save(saving=product)


    loan_info = requests.get(LOAN_API_URL).json()
    loan_baseList = loan_info.get('result').get('baseList')
    loan_optionList = loan_info.get('result').get('optionList')


    for loan_base in loan_baseList:

        fin_prdt_cd = loan_base.get('fin_prdt_cd')

        # 동일한 금융상품 존재한다면 DB에 추가하지 않음
        if Loan.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue

        save_loan = {
            'dcls_month': loan_base.get('dcls_month'), 
            'fin_co_no': loan_base.get('fin_co_no'), 
            'kor_co_nm': loan_base.get('kor_co_nm'), 
            'fin_prdt_cd': loan_base.get('fin_prdt_cd'), 
            'fin_prdt_nm': loan_base.get('fin_prdt_nm'),
            'join_way' : loan_base.get('join_way'),
            'erly_rpay_fee': loan_base.get('erly_rpay_fee'),
            'dly_rate' : loan_base.get('dly_rate'),
            'loan_lmt' : loan_base.get('loan_lmt')
        }
        
        serializer = LoanSerializer(data=save_loan)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for loan_option in loan_optionList:
    
        option_prdt_cd = loan_option.get('fin_prdt_cd')
        product = Loan.objects.get(fin_prdt_cd=option_prdt_cd)
   
        loan_option = {
            'mrtg_type': loan_option.get('mrtg_type'),
            'mrtg_type_nm' : loan_option.get('mrtg_type_nm'),
            'rpay_type_nm': loan_option.get('rpay_type_nm'), 
            'lend_rate_type_nm': loan_option.get('lend_rate_type_nm'), 
            'lend_rate_min': loan_option.get('lend_rate_min'), 
            'lend_rate_max': loan_option.get('lend_rate_max'), 
            'lend_rate_avg': loan_option.get('lend_rate_avg'), 
        }

        serializer = LoanOptionSerializer(data=loan_option)
        if serializer.is_valid(raise_exception=True):
            serializer.save(loan=product)
    return Response('complete')

# 전체 예금 목록 조회
@api_view(['GET'])
def deposit_list(request):
    deposits = Deposit.objects.all()
    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)

# 단일 예금상품 조회
@api_view(['GET'])
def deposit_detail(request, fin_prdt_cd):
    deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
    serializer = DepositSerializer(deposit)
    return Response(serializer.data)    
    
# 단일 예금상품 옵션 목록 조회 >> vue에서 언제 어디서 어떻게 사용하는지??
@api_view(['GET'])
def depositoption_list(request, fin_prdt_cd):
    deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
    deposit_options = DepositOption.objects.filter(deposit=deposit)
    serializer = DepositOptionSerializer(deposit_options, many=True)
    return Response(serializer.data)

    
# 전체 적금 목록 조회
@api_view(['GET'])
def saving_list(request):
    savings = Saving.objects.all()
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

# 단일 적금상품 조회
@api_view(['GET'])
def saving_detail(request, fin_prdt_cd):
    saving = get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)
    serializer = SavingSerializer(saving)
    return Response(serializer.data)

    
# 전체 대출 목록 조회
@api_view(['GET'])
def loan_list(request):
    loans = Loan.objects.all()
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)

# 단일 대출상품 조회
@api_view(['GET'])
def loan_detail(request, fin_prdt_cd):
    loan = get_object_or_404(Loan, fin_prdt_cd=fin_prdt_cd)
    serializer = LoanSerializer(loan)
    return Response(serializer.data) 


# 전체 금융기관 예금 금리 내림차순(예치기간 별)
@api_view(['GET'])
def get_all_deposits(request, save_trm):
    deposits = Deposit.objects.filter(depositoption__save_trm=save_trm).order_by('-depositoption__intr_rate')
    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)


# 금융기관별 예금
@api_view(['GET'])
def get_bank_deposits(request, kor_co_nm):
    if Deposit.objects.filter(kor_co_nm=kor_co_nm).exists():
        deposits = Deposit.objects.filter(kor_co_nm=kor_co_nm)
        serializer = DepositSerializer(deposits, many=True)
        return Response(serializer.data)
    else:
        return Response({ "no exist deposit product" }, status=status.HTTP_204_NO_CONTENT)
    

# 금융기관 별 예금 금리 내림차순(예치기간별)
@api_view(['GET'])
def get_reverse_deposits(request, kor_co_nm, save_trm):
    deposits = Deposit.objects.filter(Q(depositoption__save_trm=save_trm) & Q(kor_co_nm=kor_co_nm)).order_by('-depositoption__intr_rate')

    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)


# 전체 금융기관 적금 (적금유형별)
@api_view(['GET'])
def get_all_bank_savings(request, rsrv_type_nm):
    savings = Saving.objects.filter(savingoption__rsrv_type_nm=rsrv_type_nm).distinct()
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

    
# 금융기관별 적금 
@api_view(['GET'])
def get_bank_all_type_savings(request, kor_co_nm):
    savings = Saving.objects.filter(kor_co_nm=kor_co_nm)
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)
 

# 금융기관별 적금 (적금유형별)
@api_view(['GET'])
def get_bank_type_savings(request, rsrv_type_nm, kor_co_nm):
    savings = Saving.objects.filter(Q(savingoption__rsrv_type_nm=rsrv_type_nm)& Q(kor_co_nm=kor_co_nm)).distinct()
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)


# 전체 금융기관 적금 금리 내림차순(적금유형별, 예치기간별)
@api_view(['GET'])
def get_all_bank_type_reverse_savings(request, rsrv_type_nm, save_trm):
    savings = Saving.objects.filter(Q(savingoption__rsrv_type_nm=rsrv_type_nm)&Q(savingoption__save_trm=save_trm)).order_by('-savingoption__intr_rate').distinct()
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

# 금융기관 별 적금 금리 내림차순(예치기간별)
@api_view(['GET'])
def get_bank_all_type_reverse_savings(request, kor_co_nm, save_trm):
    savings = Saving.objects.filter(Q(kor_co_nm=kor_co_nm)&Q(savingoption__save_trm=save_trm)).order_by('-savingoption__intr_rate')
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)


# 전체 금융기관 적금 금리 내림차순(예치기간별)
@api_view(['GET'])
def get_all_bank_all_type_reverse_savings(request, save_trm):
    savings = Saving.objects.filter(savingoption__save_trm=save_trm).order_by('-savingoption__intr_rate')
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)


# 금융기관 별 적금 금리 내림차순(적금유형별,예치기간 별)
@api_view(['GET'])
def get_bank_type_reverse_savings(request, rsrv_type_nm, kor_co_nm, save_trm):
    savings = Saving.objects.filter(Q(savingoption__rsrv_type_nm=rsrv_type_nm)&Q(savingoption__save_trm=save_trm) & Q(kor_co_nm=kor_co_nm)).order_by('-savingoption__intr_rate').distinct()

    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)


# 예금 가입 및 가입한 예금 조회
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def deposit_contract(request, fin_prdt_cd): 
    deposit = get_object_or_404(Deposit, fin_prdt_cd = fin_prdt_cd)
    if request.method == 'GET':
        contracted_deposits = Deposit.objects.filter(contract_user=request.user)
        serializer = DepositSerializer(contracted_deposits, many=True)
        return Response(serializer.data)

    elif request.method == 'POST': 
        if request.user in deposit.contract_user.all():
            deposit.contract_user.remove(request.user)
            action = '예금 해지 완료'
        else:
            deposit.contract_user.add(request.user)
            action = '예금 가입 완료'
        response_data = {
            'action': action,
        }
        return Response(response_data)

    
# 적금 가입 및 가입한 적금 조회
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def saving_contract(request, fin_prdt_cd):
    saving = get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)

    if request.method == 'GET':
        contracted_savings = Saving.objects.filter(contract_user=request.user)
        serializer = SavingSerializer(contracted_savings, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST': 

    # 만약 권한이 있는 유저가 적금에 가입이 되어 있다면?
        if request.user in saving.contract_user.all():
            saving.contract_user.remove(request.user)
            action = '적금 해지 완료'
        else:
            saving.contract_user.add(request.user)
            action = '적금 가입 완료'

        response_data = {
            'action': action,
        }
        return Response(response_data)
    

# 대출 가입 및 가입한 대출 조회
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def loan_contract(request, fin_prdt_cd):
    loan = get_object_or_404(Loan, fin_prdt_cd=fin_prdt_cd)

    if request.method == 'GET':
        contracted_loans = Loan.objects.filter(contract_user=request.user)
        serializer = LoanSerializer(contracted_loans, many=True)
        return Response(serializer.data)
                
    elif request.method == 'POST': 

        if request.user in loan.contract_user.all():
            loan.contract_user.remove(request.user)
            action = '대출 해지 완료'
        else:
            loan.contract_user.add(request.user)
            action = '대출 가입 완료'

        response_data = {
            'action': action,
        }
        return Response(response_data)


# 가입한 예금 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deposit_contract_list(request):
    contracted_deposits = Deposit.objects.filter(contract_user=request.user)
    serializer = DepositSerializer(contracted_deposits, many=True)
    return Response(serializer.data)

    
# 가입한 적금 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saving_contract_list(request):
    contracted_savings = Saving.objects.filter(contract_user=request.user)
    serializer = SavingSerializer(contracted_savings, many=True)
    return Response(serializer.data)


# 가입한 대출 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def loan_contract_list(request):
    contracted_loans = Loan.objects.filter(contract_user=request.user)
    serializer = LoanSerializer(contracted_loans, many=True)
    return Response(serializer.data)
            


# 관심 예금 조회 및 가입
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def deposit_like(request, fin_prdt_cd):
    
    deposit = get_object_or_404(Deposit, fin_prdt_cd = fin_prdt_cd)

    if request.method == 'GET':
        liked_deposits = Deposit.objects.filter(like_user=request.user)
        serializer = DepositSerializer(liked_deposits, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST': 

        if request.user in deposit.like_user.all():
            deposit.like_user.remove(request.user)
            action = '관심 상품 삭제 완료'
        else:
            deposit.like_user.add(request.user)
            action = '관심 상품 추가 완료'

        response_data = {
            'action': action,
        }
        return Response(response_data)


# 관심 적금 조회 및 가입
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def saving_like(request, fin_prdt_cd):
    
    saving = get_object_or_404(Saving, fin_prdt_cd = fin_prdt_cd)

    if request.method == 'GET':
        liked_savings = Saving.objects.filter(like_user=request.user)
        serializer = SavingSerializer(liked_savings, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST': 

        if request.user in saving.like_user.all():
            saving.like_user.remove(request.user)
            action = '관심 상품 삭제 완료'
        else:
            saving.like_user.add(request.user)
            action = '관심 상품 추가 완료'

        response_data = {
            'action': action,
        }
        return Response(response_data)

# 관심 대출 조회 및 가입
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def loan_like(request, fin_prdt_cd):
    
    loan = get_object_or_404(Loan, fin_prdt_cd = fin_prdt_cd)

    if request.method == 'GET':
        liked_loans = Loan.objects.filter(like_user=request.user)
        serializer = LoanSerializer(liked_loans, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST': 

        if request.user in loan.like_user.all():
            loan.like_user.remove(request.user)
            action = '관심 상품 삭제 완료'
        else:
            loan.like_user.add(request.user)
            action = '관심 상품 추가 완료'

        response_data = {
            'action': action,
        }
        return Response(response_data)

# 관심 예금 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deposit_like_list(request):
    liked_deposits = Deposit.objects.filter(like_user=request.user)
    serializer = DepositSerializer(liked_deposits, many=True)
    return Response(serializer.data)

# 관심 적금 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saving_like_list(request):
    liked_savings = Saving.objects.filter(like_user=request.user)
    serializer = SavingSerializer(liked_savings, many=True)
    return Response(serializer.data)

# 관심 대출 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def loan_like_list(request):
    liked_loans = Loan.objects.filter(like_user=request.user)
    serializer = LoanSerializer(liked_loans, many=True)
    return Response(serializer.data)