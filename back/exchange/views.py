from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from .serializers import *
from .models import *
import requests



@api_view(['GET'])
def exchange_info(request):
        
        searchdate = datetime.today().strftime("%Y%m%d")
        EXCHANGE_API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&searchdate={searchdate}&data=AP01'
        exchange_infos = requests.get(EXCHANGE_API_URL).json()
        # return Response(exchange_infos)
        result = Exchange.objects.all()
   
        if exchange_infos:
                # db에 데이터가 존재X, db 저장
                if not result: 
                        serializer = ExchangeSerializer(data=exchange_infos, many=True)
                        if serializer.is_valid(raise_exception=True):          
                                serializer.save()
                        return Response(serializer.data)
                # db에 데이터가 존재O, db 데이터 삭제 후 저장
                else: 
                        Exchange.objects.all().delete()
                        serializer = ExchangeSerializer(data=exchange_infos, many=True)     
                        if serializer.is_valid(raise_exception=True):
                                serializer.save()
                                return Response(serializer.data)
        
        serializer = ExchangeSerializer(result, many=True)
        return Response(serializer.data)

       

        
