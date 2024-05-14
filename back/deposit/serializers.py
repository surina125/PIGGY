from rest_framework import serializers
from .models import *


class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_fields = ('deposit',)



class DepositSerializer(serializers.ModelSerializer):
    depositoption_set = DepositOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Deposit
        fields = '__all__'
        read_only_fields = ('contract_user','like_user')




class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        read_only_fields = ('saving',)


class SavingSerializer(serializers.ModelSerializer):
    savingoption_set = SavingOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Saving
        fields = '__all__'
        read_only_fields = ('contract_user','like_user',)



class LoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOption
        fields = '__all__'
        read_only_fields = ('loan',)


class LoanSerializer(serializers.ModelSerializer):
    loanoption_set = LoanOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('contract_user','like_user',)

# class ContractDepositSerializer(serializers.ModelSerializer):
#     depositoption_set = DepositOptionSerializer(many=True, read_only=True)
#     class Meta:
#         model = Deposit
#         fields = ('deposit_code','name', 'kor_co_nm', 'depositoption_set')


# class ContractSavingSerializer(serializers.ModelSerializer):
#     savingoption_set = SavingOptionSerializer(many=True, read_only=True)
#     class Meta:
#         model = Saving
#         fields = ('saving_code','name','kor_co_nm', 'savingoption_set')







