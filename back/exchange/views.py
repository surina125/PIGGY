from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
import requests

# Create your views here.


@api_view(['GET'])
def exchange_info(request):
        
        searchdate = datetime.today().strftime("%Y%m%d")
        EXCHANGE_API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&searchdate={searchdate}&data=AP01'
        exchange_info = requests.get(EXCHANGE_API_URL).json()
        return Response(exchange_info)