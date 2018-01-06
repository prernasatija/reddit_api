from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
import json


@csrf_exempt 
def login_view(request):
    if request.method == 'POST':
    	try:
            req = json.loads(request.body)
            username = req.get("username", '')
            password = req.get("password", '')
            user = authenticate(username=username, password=password)
            if user:
            	token, created = Token.objects.get_or_create(user=user)
            	resp= HttpResponse(content_type='application/json')
            	resp.content = json.dumps({"access_token": str(token)})
            else:
            	resp= HttpResponse(content_type='application/json', status=401)
            	resp.content = json.dumps({"error": "User not found. Incorrect username and/or password"})
            return resp
    	except Exception as e:
            resp= HttpResponse(content_type='application/json', status = 400)
            resp.content = json.dumps({"error" : str(e)})
            return resp


    else:
        resp= HttpResponse(content_type='application/json', status = 405)
        resp.content = json.dumps({"error" : "send a POST request"})
        return resp