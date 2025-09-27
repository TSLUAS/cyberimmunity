from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import ujson as json
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import time

class test(APIView):
    def get(self, request):
        print(request)
        resilt = {
            'code': 'ok',
            'message': 'hello world'
        }
        return Response(resilt)
