from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
@csrf_exempt
def odk_receive(request):
    print request.body
