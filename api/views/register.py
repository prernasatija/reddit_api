from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
#from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User
import json


@csrf_exempt 
def register(request):
    if request.method == 'PUT':
        print("inside PUT")
        #serializer = UserSerializer(data=request.data)
        #print(request.body)
        #print(type(request.body))
        #form = UserCreationForm(data = request.body)
        #print(form.errors)
        req_body = json.loads(request.body)
        username = req_body.get("username", None)

        password = req_body.get("password", None)
        #user = authenticate(username=username, password=password)
        if username and password:
            try:
                user = User.objects.create_user(username=username, password=password)
                token = Token.objects.create(user=user)
                resp= HttpResponse(content_type='application/json')
                resp.content= json.dumps({"access_token": str(token)})
                return resp
            except Exception as e:
                resp= HttpResponse(content_type='application/json', status = 401)
                resp.content = json.dumps({"error" : str(e)})
                return resp

        else:
            ret = {"error": "Both username and password are required."}
            return HttpResponse(json.dumps(ret))
    else:
        resp = HttpResponse(content_type='application/json', status = 405)
        resp.content = json.dumps({"error" : "send a PUT request"})
        return resp


