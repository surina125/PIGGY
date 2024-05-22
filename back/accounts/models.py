from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field, user_username

class User(AbstractUser):
    email = models.EmailField(max_length=300, blank=True, null=True)                                     # 이메일
    age = models.IntegerField()                                                                          # 나이
    profile_img = models.ImageField(upload_to='image/', default='image/user.png')                        # 프로필 이미지
    nickname = models.CharField(max_length=50, blank=True, null=True)                                                           # 닉네임(ID)
    annual_income = models.IntegerField(blank=True, null=True)                                           # 연봉
    property = models.IntegerField(blank=True, null=True)                                                # 자산  
    main_bank = models.CharField(max_length=50, blank=True, null=True)                                   # 주거래 은행
    D_products = models.TextField(blank=True, null=True) # 아래랑 겹치지만 필수요구사항에 있어서 우선 필드는 만들어 놓음
    S_products = models.TextField(blank=True, null=True) # 아래랑 겹치지만 필수요구사항에 있어서 우선 필드는 만들어 놓음
    L_products = models.TextField(blank=True, null=True) # 아래랑 겹치지만 필수요구사항에 있어서 우선 필드는 만들어 놓음
    ### fin_products앱 내에서 가입한 상품 목록이랑 관심상품 목록을
    ### Seposit, Saving, Loan 모델에서 User 모델과 manyTomany Field로 만들었습니다.


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")

        # 새로운 필드 추가
        nickname = data.get("nickname")
        age = data.get("age")    
        profile_img = data.get("profile_img")
        annual_income = data.get("annual_income")
        property = data.get("property")
        main_bank = data.get("main_bank")
        D_products = data.get("D_products")
        S_products = data.get("S_products")
        L_products = data.get("L_products")
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if nickname:
            user.nickname = nickname
        if age:
            user.age = age
        if profile_img:
            user.profile_img = profile_img
        if annual_income:
            user.annual_income = annual_income
        if property:
            user.property = property
        if D_products:
            user.D_products = D_products
        if S_products:
            user.S_products = S_products
        if L_products:
            user.S_products = L_products
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
    

