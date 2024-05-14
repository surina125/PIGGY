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
            'dcls_month': deposit_base.get('dcls_month','-1'), 
            'fin_co_no': deposit_base.get('fin_co_no','-1'), 
            'kor_co_nm': deposit_base.get('kor_co_nm','-1'), 
            'fin_prdt_cd': deposit_base.get('fin_prdt_cd','-1'), 
            'fin_prdt_nm': deposit_base.get('fin_prdt_nm','-1'),
            'join_way': deposit_base.get('join_way','-1'),
            'mtrt_int': deposit_base.get('mtrt_int','-1'),
            'spcl_cnd': deposit_base.get('spcl_cnd','-1'), 
            'join_deny': deposit_base.get('join_deny','-1'), 
            'join_member': deposit_base.get('join_member','-1'), 
            'etc_note': deposit_base.get('etc_note','-1'), 
            'max_limit': deposit_base.get('max_limit','-1') 
        }
        
        serializer = DepositSerializer(data=save_deposit)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for deposit_option in deposit_optionList:

        option_prdt_cd = deposit_option.get('fin_prdt_cd')
        product = Deposit.objects.get(fin_prdt_cd=option_prdt_cd)
        save_option = {
            'intr_rate_type_nm': deposit_option.get('intr_rate_type_nm', '-1'),
            'intr_rate': deposit_option.get('intr_rate', -1), 
            'intr_rate2': deposit_option.get('intr_rate2', -1), 
            'save_trm': deposit_option.get('save_trm', -1), 
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
            'dcls_month': saving_base.get('dcls_month', '-1'),
            'fin_co_no': saving_base.get('fin_co_no', '-1'),
            'kor_co_nm': saving_base.get('kor_co_nm', '-1'),
            'fin_prdt_cd': saving_base.get('fin_prdt_cd', '-1'),
            'fin_prdt_nm': saving_base.get('fin_prdt_nm', '-1'),
            'join_way': saving_base.get('join_way', '-1'),
            'mtrt_int': saving_base.get('mtrt_int', '-1'),
            'spcl_cnd': saving_base.get('spcl_cnd', '-1'),
            'join_deny': saving_base.get('join_deny', -1),
            'join_member': saving_base.get('join_member', '-1'),
            'etc_note': saving_base.get('etc_note', '-1'),
            'max_limit': saving_base.get('max_limit', -1),
        }
        serializer = SavingSerializer(data=save_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for save_option in saving_optionList:
        option_prdt_cd = save_option.get('fin_prdt_cd', '-1')
        product = Saving.objects.get(fin_prdt_cd=option_prdt_cd)
        save_option = {
            'intr_rate_type': save_option.get('intr_rate_type', '-1'),
            'intr_rate_type_nm': save_option.get('intr_rate_type_nm', '-1'),
            'intr_rate': save_option.get('intr_rate', -1),
            'intr_rate2': save_option.get('intr_rate2', -1),
            'save_trm': save_option.get('save_trm', -1),
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
            'dcls_month': loan_base.get('dcls_month','-1'), 
            'fin_co_no': loan_base.get('fin_co_no','-1'), 
            'kor_co_nm': loan_base.get('kor_co_nm','-1'), 
            'fin_prdt_cd': loan_base.get('fin_prdt_cd','-1'), 
            'fin_prdt_nm': loan_base.get('fin_prdt_nm','-1'),
            'erly_rpay_fee': loan_base.get('erly_rpay_fee','-1'),
            'dly_rate' : loan_base.get('dly_rate','-1'),
            'loan_lmt' : loan_base.get('loan_lmt','-1')
        }
        
        serializer = LoanSerializer(data=save_loan)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for loan_option in loan_optionList:
    
        option_prdt_cd = loan_option.get('fin_prdt_cd')
        product = Loan.objects.get(fin_prdt_cd=option_prdt_cd)
   
        loan_option = {
            'imrtg_type_nm': loan_option.get('imrtg_type_nm', '-1'),
            'rpay_type_nm': loan_option.get('rpay_type_nm', -1), 
            'lend_rate_type_nm': loan_option.get('lend_rate_type_nm', -1), 
            'lend_rate_min': loan_option.get('lend_rate_min', -1), 
            'lend_rate_max': loan_option.get('lend_rate_max', -1), 
            'lend_rate_avg': loan_option.get('lend_rate_avg', -1), 
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
def deposit_detail(request, deposit_code):
    deposit = get_object_or_404(Deposit, fin_prdt_cd=deposit_code)
    if request.method == 'GET':
        serializer = DepositSerializer(deposit)
        return Response(serializer.data)    
    
# 단일 예금상품 금리 조회
@api_view(['GET'])
def depositOption_list(request, deposit_code):
    deposit = get_object_or_404(Deposit, fin_prdt_cd=deposit_code)
    deposit_options = DepositOption.objects.filter(deposit=deposit)

    # if request.method == 'GET':
    serializer = DepositOptionSerializer(deposit_options, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# def depositOption_detail(request, deposit_code, depositOption_pk):
#     deposit = get_object_or_404(Deposit, deposit_code=deposit_code)
#     deposit_option = get_object_or_404(DepositOption, pk=depositOption_pk, deposit=deposit)

#     if request.method == 'GET':
#         serializer = DepositOptionSerializer(deposit_option)
#         return Response(serializer.data)
    

# @api_view(['GET']) # id 순
# def saving_list(request):
#     savings = Saving.objects.all()
#     serializer = SavingSerializer(savings, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def saving_detail(request, saving_code):
#     saving = get_object_or_404(Saving, saving_code=saving_code)
#     if request.method == 'GET':
#         serializer = SavingSerializer(saving)
#         return Response(serializer.data)

    
# @api_view(['GET'])
# def savingOption_list(request, saving_code):
#     saving = get_object_or_404(Saving, saving_code=saving_code)
#     saving_options = SavingOption.objects.filter(saving=saving)

#     if request.method == 'GET':
#         serializer = SavingOptionSerializer(saving_options, many=True)
#         return Response(serializer.data)


# @api_view(['GET'])
# def savingOption_detail(request, saving_code, savingOption_pk):
#     savingOption = get_object_or_404(SavingOption, pk=savingOption_pk)
#     if request.method == 'GET':
#         serializer = SavingOptionSerializer(savingOption)
#         return Response(serializer.data)
    

# # 6개월~36개월
# @api_view(['GET'])
# def get_deposits(request, save_trm):
#     deposits = Deposit.objects.filter(depositoption__save_trm=save_trm).order_by('depositoption__intr_rate')

#     serializer = DepositSerializer(deposits, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def get_savings(request, save_trm):
#     savings = Saving.objects.filter(savingoption__save_trm=save_trm).order_by('savingoption__intr_rate')

#     serializer = SavingSerializer(savings, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def get_reverse_deposits(request, save_trm):
#     deposits = Deposit.objects.filter(depositoption__save_trm=save_trm).order_by('-depositoption__intr_rate')

#     serializer = DepositSerializer(deposits, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def get_reverse_savings(request, save_trm):
#     savings = Saving.objects.filter(savingoption__save_trm=save_trm).order_by('-savingoption__intr_rate')

#     serializer = SavingSerializer(savings, many=True)
#     return Response(serializer.data)



# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def contract_deposit(request, deposit_code):
#     deposit = get_object_or_404(Deposit, deposit_code=deposit_code)
#     if request.user in deposit.contract_user.all():
#         deposit.contract_user.remove(request.user)
#     else:
#         deposit.contract_user.add(request.user)
#     serializer = ContractDepositSerializer(deposit)
#     return Response(serializer.data)


# @api_view(['GET','POST','DELETE'])
# @permission_classes([IsAuthenticated])
# def contract_deposit(request, deposit_code):
#     deposit = get_object_or_404(Deposit, deposit_code=deposit_code)
#     if request.method == 'GET':
#         serializer = ContractDepositSerializer(deposit)
#         return Response(serializer.data)

#     elif request.method == 'DELETE':
#         if request.user in deposit.contract_user.all():
#             deposit.contract_user.remove(request.user)
#             return Response({ "detail": "삭제되었습니다." }, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({ "detail": "삭제할 항목이 없습니다." }, status=status.HTTP_404_NOT_FOUND)
        
#     elif request.method == 'POST':
#         if request.user not in deposit.contract_user.all():
#             deposit.contract_user.add(request.user)
#             serializer = ContractDepositSerializer(deposit, data=request.data, partial=True)

#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 return Response({ "detail": "상품이 추가되었습니다." }, status=status.HTTP_200_OK)
#         else:
#             return Response({ "detail": "이미 상품이 존재합니다." }, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['GET','POST','DELETE'])
# @permission_classes([IsAuthenticated])
# def contract_saving(request, saving_code):
#     saving = get_object_or_404(Saving, saving_code=saving_code)
#     if request.method == 'GET':
#         serializer = ContractSavingSerializer(saving)
#         return Response(serializer.data)
    
#     elif request.method == 'DELETE':
#         if request.user in saving.contract_user.all():
#             saving.contract_user.remove(request.user)
#             return Response({ "detail": "삭제되었습니다." }, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({ "detail": "삭제할 항목이 없습니다." }, status=status.HTTP_404_NOT_FOUND)
        
#     elif request.method == 'POST':
#         if request.user not in saving.contract_user.all():
#             saving.contract_user.add(request.user)
#             serializer = ContractSavingSerializer(saving, data=request.data, partial=True)

#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 return Response({ "detail": "상품이 추가되었습니다." }, status=status.HTTP_200_OK)
#         else:
#             return Response({ "detail": "이미 상품이 존재합니다." }, status=status.HTTP_400_BAD_REQUEST)
        

# @api_view(['GET'])
# def get_bank_deposit(request, kor_co_nm):
#     if Deposit.objects.filter(kor_co_nm=kor_co_nm).exists():
#         deposits = Deposit.objects.filter(kor_co_nm=kor_co_nm)
#         serializer = DepositSerializer(deposits, many=True)
#         return Response(serializer.data)
#     else:
#         return Response({ "detail": "해당은행의 상품이 없습니다.." }, status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# def get_bank_saving(request, kor_co_nm):
#     if Saving.objects.filter(kor_co_nm=kor_co_nm).exists():
#         savings = Saving.objects.filter(kor_co_nm=kor_co_nm)
#         serializer = SavingSerializer(savings, many=True)
#         return Response(serializer.data)
#     else:
#         return Response({ "detail": "해당은행의 상품이 없습니다.." }, status=status.HTTP_204_NO_CONTENT)
    
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def recommend_product_one(request):
#     user = get_object_or_404(User, username=request.user.username)
#     desired_amount_deposit = user.desire_amount_deposit
#     desired_period_deposit = user.deposit_period

#     if not desired_period_deposit or not desired_amount_deposit:
#         if not desired_period_deposit:
#             return Response({"message": "유저의 희망기간이 없습니다."})
#         elif not desired_amount_deposit:
#             return Response({"message": "유저의 희망적금금액이 없습니다."})