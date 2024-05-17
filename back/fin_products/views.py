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
# from accounts.models import User
import requests
from .serializers import *
from .models import *
# from accounts.serializers import *


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
    # return Response(saving_optionList)


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
def deposit_detail(request, code):
    deposit = get_object_or_404(Deposit, fin_prdt_cd=code)
    serializer = DepositSerializer(deposit)
    return Response(serializer.data)    
    
# 단일 예금상품 옵션 목록 조회 >> vue에서 언제 어디서 어떻게 사용하는지??
@api_view(['GET'])
def depositoption_list(request, code):
    deposit = get_object_or_404(Deposit, fin_prdt_cd=code)
    deposit_options = DepositOption.objects.filter(deposit=deposit)
    serializer = DepositOptionSerializer(deposit_options, many=True)
    return Response(serializer.data)

# 단일 예금상품 옵션 조회
@api_view(['GET'])
def depositoption_detail(request, code, option_pk):
    deposit = get_object_or_404(Deposit, fin_prdt_cd=code)
    deposit_option = get_object_or_404(DepositOption, pk=option_pk, deposit=deposit)
    serializer = DepositOptionSerializer(deposit_option)
    return Response(serializer.data)
    
# 전체 적금 목록 조회
@api_view(['GET']) 
def saving_list(request):
    savings = Saving.objects.all()
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

# 단일 적금상품 조회
@api_view(['GET'])
def saving_detail(request, code):
    saving = get_object_or_404(Saving, fin_prdt_cd=code)
    serializer = SavingSerializer(saving)
    return Response(serializer.data)

# 단일 적금상품 옵션 목록 조회    
@api_view(['GET'])
def savingoption_list(request, code):
    saving = get_object_or_404(Saving, fin_prdt_cd=code)
    saving_options = SavingOption.objects.filter(saving=saving)
    serializer = SavingOptionSerializer(saving_options, many=True)
    return Response(serializer.data)

# 단일 적금상품 옵션 조회
@api_view(['GET'])
def savingoption_detail(request, code, option_pk):
    savingOption = get_object_or_404(SavingOption, pk=option_pk)
    serializer = SavingOptionSerializer(savingOption)
    return Response(serializer.data)
    
# 전체 대출 목록 조회
@api_view(['GET']) 
def loan_list(request):
    loans = Loan.objects.all()
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)

# 단일 대출상품 조회
@api_view(['GET'])
def loan_detail(request, code):
    loan = get_object_or_404(Loan, fin_prdt_cd=code)
    serializer = LoanSerializer(loan)
    return Response(serializer.data) 

# 단일 대출상품 옵션 목록 조회
@api_view(['GET'])
def loanoption_list(request, code):
    loan = get_object_or_404(Loan, fin_prdt_cd=code)
    loan_options = LoanOption.objects.filter(loan=loan)
    serializer = LoanOptionSerializer(loan_options, many=True)
    return Response(serializer.data)

# 단일 대출상품 옵션 조회
@api_view(['GET'])
def loanoption_detail(request, code, option_pk):
    loan = get_object_or_404(Loan, fin_prdt_cd=code)
    loan_option = get_object_or_404(LoanOption, pk=option_pk, loan=loan)
    serializer = LoanOptionSerializer(loan_option)
    return Response(serializer.data)

# 전체 금융기관 예금 금리 내림차순(예치기간 별)
@api_view(['GET'])
def get_all_reverse_deposits(request, save_trm):
    deposits = Deposit.objects.filter(depositoption__save_trm=save_trm).order_by('-depositoption__intr_rate')
    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)
    
# 금융기관 별 예금 금리 내림차순(예치기간 별)
@api_view(['GET'])
def get_reverse_deposits(request, kor_co_nm, save_trm):
    deposits = Deposit.objects.filter(Q(depositoption__save_trm=save_trm) & Q(kor_co_nm=kor_co_nm)).order_by('-depositoption__intr_rate')

    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)

# 전체 금융기관 적금 금리 내림차순(예치기간 별)
@api_view(['GET'])
def get_all_reverse_savings(request, save_trm):
    savings = Saving.objects.filter(savingoption__save_trm=save_trm).order_by('-savingoption__intr_rate')
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

# 금융기관 별 적금 금리 내림차순(예치기간 별)
@api_view(['GET'])
def get_reverse_savings(request, kor_co_nm, save_trm):
    savings = Saving.objects.filter(Q(savingoption__save_trm=save_trm) & Q(kor_co_nm=kor_co_nm)).order_by('-savingoption__intr_rate')

    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

# # 전체 금융기관 대출 금리 내림차순(예치기간 별)
# @api_view(['GET'])
# def get_aes_loans(request, mrtg_type):
#     loans = Loan.objects.filter(loanoption__mrtg_type=mrtg_type).order_by('loanoption__lend_rate_min')
#     serializer = LoanSerializer(loans, many=True)
#     return Response(serializer.data)


# 금융기관 별 최저 대출 금리 오름차순(담보유형)
@api_view(['GET'])
def get_min_loans(request, kor_co_nm, mrtg_type):
    loans = Loan.objects.filter(Q(loanoption__mrtg_type=mrtg_type) & Q(kor_co_nm=kor_co_nm)).order_by('loanoption__lend_rate_min')
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)


# 금융기관 별 최대 대출 금리 오름차순(담보유형)
@api_view(['GET'])
def get_max_loans(request, kor_co_nm, mrtg_type):
    loans = Loan.objects.filter(Q(loanoption__mrtg_type=mrtg_type) & Q(kor_co_nm=kor_co_nm)).order_by('loanoption__lend_rate_max')
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)

# 금융기관 별 평균 대출 금리 오름차순(담보유형)
@api_view(['GET'])
def get_avg_loans(request, kor_co_nm, mrtg_type):
    loans = Loan.objects.filter(Q(loanoption__mrtg_type=mrtg_type) & Q(kor_co_nm=kor_co_nm)).order_by('loanoption__lend_rate_avg')
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)

# 금융기관 별 예금상품
@api_view(['GET'])
def deposit_bank(request, kor_co_nm):
    if Deposit.objects.filter(kor_co_nm=kor_co_nm).exists():
        deposits = Deposit.objects.filter(kor_co_nm=kor_co_nm)
        serializer = DepositSerializer(deposits, many=True)
        return Response(serializer.data)
    else:
        return Response({ "no exist loan product" }, status=status.HTTP_204_NO_CONTENT)

# 금융기관 별 적금상품
@api_view(['GET'])
def saving_bank(request, kor_co_nm):
    if Saving.objects.filter(kor_co_nm=kor_co_nm).exists():
        savings = Saving.objects.filter(kor_co_nm=kor_co_nm)
        serializer = SavingSerializer(savings, many=True)
        return Response(serializer.data)
    else:
        return Response({"no exist loan product"}, status=status.HTTP_204_NO_CONTENT)
    
# 금융기관 별 대출상품
@api_view(['GET'])
def loan_bank(request, kor_co_nm):
    if Loan.objects.filter(kor_co_nm=kor_co_nm).exists():
        loans = Loan.objects.filter(kor_co_nm=kor_co_nm)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
    else:
        return Response({"no exist loan product"}, status=status.HTTP_204_NO_CONTENT)
    

# 예금 가입 및 가입한 예금 조회
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def deposit_contract(request, code):
    
    deposit = get_object_or_404(Deposit, fin_prdt_cd = code)

    if request.method == 'GET':
        # 유저가 적금에 가입되어 있는지 확인
        if request.user in deposit.contract_user.all():
            # 해당 유저의 가입 정보 가져오기
            contracted_parts = deposit.contract_user.objects.filter(user_id=request.user)

            # 가입된 적금에 대한 정보를 저장할 리스트
            contract_data = []

            # 가입된 적금에 대한 입금 정보 가져오기
            for deposit in Deposit.objects.all():
                # 가입된 적금과 관련된 입금 정보인지 확인
                if deposit.id in contracted_parts.values_list('deposit_id', flat=True):
                    # 입금 정보를 사전 형태로 구성하여 리스트에 추가
                    deposit_data = {
                        'id': deposit.id,
                        'amount': deposit.amount,
                        # 필요한 다른 입금 정보도 여기에 추가
                    }
                    contract_data.append(deposit_data)

            # 결과를 시리얼라이즈하고 반환
            serializer = DepositSerializer(contract_data, many=True)
            return Response(serializer.data)
        else:
            # 가입되지 않은 경우에 대한 처리
            return Response({'message': 'User is not contracted to this saving.'})
        
    elif request.method == 'POST': 

    # 만약 권한이 있는 유저가 적금에 가입이 되어 있다면?
        if request.user in deposit.contract_user.all():
            deposit.contract_user.remove(request.user)
            action = '적금 해지 완료'
        else:
            deposit.contract_user.add(request.user)
            action = '적금 가입 완료'

        response_data = {
            'action': action,
        }
        return Response(response_data)

    # 만약 권한이 있는 유저가 예금에 가입이 되어 있다면?
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
def saving_contract(request, code):
    saving = get_object_or_404(Saving, fin_prdt_cd=code)

    if request.method == 'GET':
        # 유저가 적금에 가입되어 있는지 확인
        if request.user in saving.contract_user.all():
            # 해당 유저의 가입 정보 가져오기
            contracted_parts = saving.contract_user.objects.filter(user_id=request.user)

            # 가입된 적금에 대한 정보를 저장할 리스트
            contract_data = []

            # 가입된 적금에 대한 입금 정보 가져오기
            for saving in Saving.objects.all():
                # 가입된 적금과 관련된 입금 정보인지 확인
                if saving.id in contracted_parts.values_list('saving_id', flat=True):
                    # 입금 정보를 사전 형태로 구성하여 리스트에 추가
                    saving_data = {
                        'id': saving.id,
                        'amount': saving.amount,
                        # 필요한 다른 입금 정보도 여기에 추가
                    }
                    contract_data.append(saving_data)

            # 결과를 시리얼라이즈하고 반환
            serializer = SavingSerializer(contract_data, many=True)
            return Response(serializer.data)
        else:
            # 가입되지 않은 경우에 대한 처리
            return Response({'message': 'User is not contracted to this saving.'})
        
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




# 대출 가입
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def loan_contract(request, code):
    loan = get_object_or_404(Loan, fin_prdt_cd=code)

    # 만약 권한이 있는 유저가 대출에 가입이 되어 있다면?
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



