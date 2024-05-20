from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import UserInfoSerializer, UserProfileSerializer
import pandas as pd
import json


User = get_user_model()

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_info(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.user.username != username:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = UserInfoSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def recommend(request, username):
    # 데이터베이스에서 모델의 모든 객체를 쿼리셋으로 불러오기
    # 필요한 칼럼만 선택
    queryset = User.objects.all().values(
        'id', 'username', 'age', 'annual_income', 'property', 'D_products', 'S_products', 'L_products'
    )

    # 쿼리셋을 리스트의 딕셔너리 형태로 변환
    data = list(queryset)

    # 데이터프레임으로 변환할 때 필요한 칼럼만 선택
    df = pd.DataFrame(data, 
    columns=['id', 'username', 'age', 'annual_income', 'property', 'D_products', 'S_products', 'L_products'])

    # 입력된 사용자의 데이터 가져오기
    user_data = df[df['username'] == username]

    if user_data.empty:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # 입력된 사용자를 제외한 다른 사용자들의 데이터 가져오기
    other_users = df[df['username'] != username]

    # 유사도 계산 (여기서는 유클리드 거리 사용)
    user_vector = user_data[['annual_income', 'property']].values[0]
    other_users['distance'] = other_users.apply(lambda row: euclidean(user_vector, [row['annual_income'], row['property']]), axis=1)

    # 가장 비슷한 사용자 찾기 (거리가 가장 작은 사용자)
    most_similar_user = other_users.loc[other_users['distance'].idxmin()]

    # 결과를 JSON 형태로 반환
    result = {
        'id': most_similar_user['id'],
        'username': most_similar_user['username'],
        'age': most_similar_user['age'],
        'annual_income': most_similar_user['annual_income'],
        'property': most_similar_user['property'],
        'D_products': most_similar_user['D_products'],
        'S_products': most_similar_user['S_products'],
        'L_products': most_similar_user['L_products']
    }

    return Response(result, status=status.HTTP_200_OK)

    # # 데이터베이스에서 모델의 모든 객체를 쿼리셋으로 불러오기
    # # 필요한 칼럼만 선택
    # queryset = User.objects.all().values(
    #     'id', 'username', 'age', 'annual_income', 'property', 'D_products', 'S_products', 'L_products'
    # )

    # # 쿼리셋을 리스트의 딕셔너리 형태로 변환
    # data = list(queryset)

    # # 데이터프레임으로 변환할 때 필요한 칼럼만 선택
    # df = pd.DataFrame(data, columns=['id', 'username', 'age', 'annual_income', 'property', 'D_products', 'S_products', 'L_products'])

    # # 입력된 사용자의 데이터 가져오기
    # user_data = df[df['username'] == username]

    # if user_data.empty:
    #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # # 입력된 사용자를 제외한 다른 사용자들의 데이터 가져오기
    # other_users = df[df['username'] != username]

    # # 유클리드 거리 계산 (나이, 연봉, 자산 사용)
    # user_vector = user_data[['age', 'annual_income', 'property']].values[0]
    # other_users['distance'] = other_users.apply(lambda row: euclidean(user_vector, [row['age'], row['annual_income'], row['property']]), axis=1)

    # # 가장 비슷한 사용자 찾기 (거리가 가장 작은 사용자)
    # most_similar_user = other_users.loc[other_users['distance'].idxmin()]

    # # 결과를 JSON 형태로 반환
    # result = {
    #     'id': most_similar_user['id'],
    #     'username': most_similar_user['username'],
    #     'age': most_similar_user['age'],
    #     'annual_income': most_similar_user['annual_income'],
    #     'property': most_similar_user['property'],
    #     'D_products': most_similar_user['D_products'],
    #     'S_products': most_similar_user['S_products'],
    #     'L_products': most_similar_user['L_products']
    # }

    # return Response(result, status=status.HTTP_200_OK)
    

        
