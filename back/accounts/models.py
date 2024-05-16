from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field, user_username

class User(AbstractUser):
    SAVING_PROPENSITY_CHOICES = [
        ('알뜰형', '알뜰형'),
        ('도전형', '도전형'),
        ('성실형', '성실형'),
    ]

    email = models.EmailField(max_length=300, blank=True, null=True)                                     # 이메일
    profile_img = models.ImageField(upload_to='image/', default='image/user.png')                        # 프로필 이미지
    is_superuser = models.BooleanField(default=False)                                                    # 관리자 아닐 경우 default 부여
    nickname = models.CharField(max_length=50, unique=True)                                              # 닉네임(ID)
    annual_income = models.IntegerField(blank=True, null=True)                                           # 연봉
    property = models.IntegerField(blank=True, null=True)                                                # 자산  
    main_bank = models.CharField(max_length=50, blank=True, null=True)                                   # 주거래 은행
    saving_propensity = models.CharField(max_length=20, choices=SAVING_PROPENSITY_CHOICES)               # 성향



class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        # 새로운 필드 추가
        nickname = data.get("nickname")
        profile_img = data.get("profile_img")
        contract_products = data.get("contract_products")
        like_products = data.get("like_products")
        annual_income = data.get("annual_income")
        property = data.get("property")
        main_bank = data.get("main_bank")
        saving_propensity = data.get("saving_propensity")
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if nickname:
            user.nickname = nickname
        if profile_img:
            user.profile_img = profile_img
        if contract_products:
            user.contract_products = contract_products
        if like_products:
            user.like_products = like_products
        if annual_income:
            user.annual_income = annual_income
        if property:
            user.property = property
        if saving_propensity:
            user.saving_propensity = saving_propensity
        if main_bank:
            user.main_bank = main_bank
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user
    

