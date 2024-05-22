from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import UserInfoSerializer, UserProfileSerializer
import pandas as pd
from scipy.spatial.distance import euclidean


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
    

# 첫번째 추천 방법 (시간 비교 - 1. sort 또는 2. 가장 작은것 찾은 다음 10개 안채워지면 userdrop하고 다음 가장 작은 사람 찾기)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend(request, username):
    # 데이터베이스에서 모델의 모든 객체를 쿼리셋으로 불러오기
    queryset = User.objects.all().values(
        'id', 'username', 'age', 'annual_income', 'property', 'D_products', 'S_products', 'L_products'
    )

    # 쿼리셋을 리스트의 딕셔너리 형태로 변환
    data = list(queryset)

    # 데이터프레임으로 변환할 때 필요한 칼럼만 선택
    df = pd.DataFrame(data, columns=['id', 'username', 'age', 'annual_income', 'property', 'D_products', 'S_products', 'L_products'])

    # 입력된 사용자의 데이터 가져오기
    user_data = df[df['username'] == username]

    if user_data.empty:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # 입력 사용자의 원래 제품 목록 저장, None 값을 빈 문자열로 대체
    user_D_products = set(user_data['D_products'].values[0].split(',') if user_data['D_products'].values[0] else [])
    user_S_products = set(user_data['S_products'].values[0].split(',') if user_data['S_products'].values[0] else [])
    user_L_products = set(user_data['L_products'].values[0].split(',') if user_data['L_products'].values[0] else [])

    # 입력된 사용자를 제외한 다른 사용자들의 데이터 가져오기
    other_users = df[df['username'] != username]

    # 입력 사용자의 벡터
    user_vector = user_data[['age', 'annual_income', 'property']].values[0]

    # 제품 목록을 중복 없이 합치기 위한 집합
    recommended_products = {
        'D_products': set(),
        'S_products': set(),
        'L_products': set()
    }

    # 비슷한 사용자들로부터 제품 목록을 채우기
    while len(recommended_products['D_products']) + len(recommended_products['S_products']) + len(recommended_products['L_products']) < 10 and not other_users.empty:
        # 거리 계산 및 가장 가까운 사용자 찾기
        other_users['distance'] = other_users.apply(lambda row: euclidean(user_vector, [row['age'], row['annual_income'], row['property']]), axis=1)
        closest_user = other_users.loc[other_users['distance'].idxmin()]

        # 추천 제품 목록 업데이트
        recommended_products['D_products'].update(set(closest_user['D_products'].split(',') if closest_user['D_products'] else []) - user_D_products)
        recommended_products['S_products'].update(set(closest_user['S_products'].split(',') if closest_user['S_products'] else []) - user_S_products)
        recommended_products['L_products'].update(set(closest_user['L_products'].split(',') if closest_user['L_products'] else []) - user_L_products)

        # 가장 가까운 사용자 제거
        other_users = other_users.drop(closest_user.name)

    # 결과를 JSON 형태로 반환
    result = {
        'D_products': list(recommended_products['D_products']),
        'S_products': list(recommended_products['S_products']),
        'L_products': list(recommended_products['L_products'])
    }

    return Response(result, status=status.HTTP_200_OK)

    # 데이터베이스에서 모델의 모든 객체를 쿼리셋으로 불러오기
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

    # # 입력 사용자의 원래 제품 목록 저장, None 값을 빈 문자열로 대체
    # user_D_products = set(user_data['D_products'].values[0].split(',') if user_data['D_products'].values[0] else [])
    # user_S_products = set(user_data['S_products'].values[0].split(',') if user_data['S_products'].values[0] else [])
    # user_L_products = set(user_data['L_products'].values[0].split(',') if user_data['L_products'].values[0] else [])

    # # 입력된 사용자를 제외한 다른 사용자들의 데이터 가져오기
    # other_users = df[df['username'] != username]

    # # 입력 사용자의 벡터
    # user_vector = user_data[['age', 'annual_income', 'property']].values[0]

    # # 거리 계산 및 정렬
    # other_users['distance'] = other_users.apply(lambda row: euclidean(user_vector, [row['age'], row['annual_income'], row['property']]), axis=1)
    # other_users = other_users.sort_values('distance')

    # # 제품 목록을 중복 없이 합치기 위한 집합
    # recommended_products = {
    #     'D_products': set(),
    #     'S_products': set(),
    #     'L_products': set()
    # }

    # # 비슷한 사용자들로부터 제품 목록을 채우기
    # for _, row in other_users.iterrows():
    #     recommended_products['D_products'].update(set(row['D_products'].split(',') if row['D_products'] else []) - user_D_products)
    #     recommended_products['S_products'].update(set(row['S_products'].split(',') if row['S_products'] else []) - user_S_products)
    #     recommended_products['L_products'].update(set(row['L_products'].split(',') if row['L_products'] else []) - user_L_products)

    #     total_products = len(recommended_products['D_products']) + len(recommended_products['S_products']) + len(recommended_products['L_products'])
    #     if total_products >= 10:
    #         break

    # # 결과를 JSON 형태로 반환
    # result = {
    #     'D_products': list(recommended_products['D_products']),
    #     'S_products': list(recommended_products['S_products']),
    #     'L_products': list(recommended_products['L_products'])
    # }

    # return Response(result, status=status.HTTP_200_OK)
