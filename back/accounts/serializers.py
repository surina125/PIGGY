from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer


class CustomRegisterSerializer(RegisterSerializer):
    # 필요한 필드들을 추가합니다.
    nickname = serializers.CharField(
        required=False,
        max_length=50
    )
    annual_income = serializers.IntegerField(
        required=False,
    )
    property = serializers.IntegerField(
        required=False,
    )
    main_bank = serializers.CharField(
        max_length=50,
        required=False,
    )
    age = serializers.IntegerField(
        required=False,
    )
    saving_propensity = serializers.ChoiceField(choices=User.SAVING_PROPENSITY_CHOICES)
    profile_img = serializers.ImageField(required=False)
    
    # 해당 필드도 저장 시 함께 사용하도록 설정합니다.
    def get_cleaned_data(self):
        return {
        'username': self.validated_data.get('username', ''),
        'password1': self.validated_data.get('password1', ''),
        # 추가한 필드
        'nickname': self.validated_data.get('nickname', ''),
        'age': self.validated_data.get('age', ''),
        'annual_income': self.validated_data.get('annual_income', ''),
        'email': self.validated_data.get('email', ''),
        'property': self.validated_data.get('property', ''),
        'main_bank': self.validated_data.get('main_bank', ''),
        'saving_propensity': self.validated_data.get('saving_propensity', ''),
        'profile_img': self.validated_data.get('profile_img', ''),
        }
    

UserModel = get_user_model()
class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'nickname'):
            extra_fields.append('nickname')
        if hasattr(UserModel, 'annual_income'):
            extra_fields.append('annual_income')
        if hasattr(UserModel, 'property'):
            extra_fields.append('property')
        if hasattr(UserModel, 'main_bank'):
            extra_fields.append('main_bank')
        if hasattr(UserModel, 'saving_propensity'):
            extra_fields.append('saving_propensity')
        if hasattr(UserModel, 'profile_img'):
            extra_fields.append('profile_img')

            model = UserModel
            fields = ('pk', *extra_fields)
            read_only_fields = ('email',)

