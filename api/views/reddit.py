from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
import requests
from api.models import models
import json

@csrf_exempt
def reddit(request):
	if request.method == 'GET':
		if not request.GET.get('access_token'):
			resp = HttpResponse(content_type='application/json', status=400)
			resp.content = json.dumps({"error" : "missing access_token"})
			return resp
		token = Token.objects.filter(key=request.GET.get('access_token'))
		if not token:
			resp = HttpResponse(content_type='application/json', status=400)
			resp.content = json.dumps({"error": "invalid access_token"})
			return resp
		attempt = 0
		while attempt < 30:
			attempt = attempt + 1
			r = requests.get('https://www.reddit.com/hot.json')
			if r.status_code == 200:
				reddit_data = r.json()
				all_links = []
				for child in reddit_data['data']['children']:
					tmp_dict = {}
					tmp_dict['reddit_id'] = child['data']['id']
					tmp_dict['permalink'] = child['data']['permalink']
					tmp_dict['url'] = child['data']['url']
					tmp_dict['author'] = child['data']['author']
					all_links.append(tmp_dict)
					# now save this locally
					try:
						article = models.Article()
						article.url = tmp_dict['url']
						article.reddit_id = tmp_dict['reddit_id']
						article.permalink = tmp_dict['permalink']
						article.url = tmp_dict['url']
						article.author = tmp_dict['author']
						article.save()
					except:
						# to avoid saving dupicate article in the db.
						continue
				return HttpResponse(json.dumps(all_links))
			else:
				if attempt == 30:
					resp = HttpResponse(content_type='application/json', status=403)
					resp.content = json.dumps({"error" : "page not found, getting code : {}".format(r.status_code)})
					return resp
		resp = HttpResponse(content_type='application/json', status=405)
		resp.content = json.dumps({"error": "send a GET request"})
		return resp
			

@csrf_exempt
def favorite(request):
	if request.method == 'PUT':
		#tokens= Token.objects.all
		req_body = json.loads(request.body)
		if 'access_token' not in req_body:
			resp = HttpResponse(content_type='application/json', status=400)
			resp.content = json.dumps({"error" : "access_token is required"})
			return resp
		if 'reddit_id' not in req_body:
			resp = HttpResponse(content_type='application/json', status=400)
			resp.content = json.dumps({"error" : "reddit_id is required"})
			return resp
		token = Token.objects.filter(key=req_body.get("access_token"))
		if not token:
			resp = HttpResponse(content_type='application/json', status=400)
			resp.content = json.dumps({"error": "invalid access_token"})
			return resp
		print(token)
		reddit_id = req_body.get("reddit_id")
		article_tags = req_body.get("tags")
		if token and reddit_id:
			favorite = models.Favorite()
			favorite.user_id = token[0].user_id
			favorite.reddit_id = reddit_id
			favorite.save()
			if article_tags:
				for tag in article_tags:
					t = models.Tags()
					t.tag = tag
					t.favorite_id = favorite.id
					t.save()
			resp = HttpResponse(content_type='application/json')
			resp.content = json.dumps({"msg" : "Article successfully favorited and tagged"})
		else:
			resp = HttpResponse(content_type='application/json', status=401)
			resp.content = json.dumps({"error" : "invalid token or reddit_id"})
		return resp
	else:
		resp = HttpResponse(content_type='application/json', status = 405)
		resp.content = json.dumps({"error" : "send a PUT request"})
		return resp


@csrf_exempt
def favorites(request):
	if request.method == 'GET':
		if not request.GET.get('access_token'):
			resp = HttpResponse(content_type='application/json', status=400)
			resp.content = json.dumps({"error" : "missing access_token"})
			return resp
		token = Token.objects.filter(key=request.GET.get('access_token'))
		if not token:
			resp = HttpResponse(content_type='application/json', status=400)
			resp.content = json.dumps({"error": "invalid access_token"})
			return resp
		#valid access_token now fetch the information
		favs = models.Favorite.objects.filter(user_id=token[0].user_id)
		ret = []
		for fav in favs:
			try:
				article = models.Article.objects.get(reddit_id = fav.reddit_id)
				record = {}
				record['reddit_id'] = fav.reddit_id
				record['permalink'] = article.permalink
				record['url'] = article.url
				record['author'] = article.author
				record_tags = []
				for tag_obj in models.Tags.objects.filter(favorite_id = fav.id):
					record_tags.append(tag_obj.tag)
				record['tags'] = record_tags
				ret.append(record)
			except:
				continue
		resp = HttpResponse(content_type='application/json')
		resp.content = json.dumps(ret)
		return resp

	else:
		resp = HttpResponse(content_type='application/json', status = 405)
		resp.content = json.dumps({"error" : "send a GET request"})
		return resp


@csrf_exempt
def tag(request):
	if request.method == 'GET':
		if not request.GET.get('access_token'):
			resp = HttpResponse(content_type='application/json', status=400)
			resp.content = json.dumps({"error" : "missing access_token"})
			return resp
		if not request.GET.get('tag'):
			resp = HttpResponse(content_type='application/json', status=400)
			resp.content = json.dumps({"error" : "missing tag"})
			return resp
		token = Token.objects.filter(key=request.GET.get('access_token'))
		if not token:
			resp = HttpResponse(content_type='application/json', status=400)
			resp.content = json.dumps({"error": "invalid access_token"})
			return resp
		#valid access_token now fetch the information
		ret = []
		for tag in models.Tags.objects.filter(tag=request.GET.get('tag')):
			favs = models.Favorite.objects.filter(id=tag.favorite_id, user_id=token[0].user_id)
			for fav in favs:
				try:
					article = models.Article.objects.get(reddit_id = fav.reddit_id)
					record = {}
					record['reddit_id'] = fav.reddit_id
					record['permalink'] = article.permalink
					record['url'] = article.url
					record['author'] = article.author
					record_tags = []
					for tag_obj in models.Tags.objects.filter(favorite_id = fav.id):
						record_tags.append(tag_obj.tag)
					record['tags'] = record_tags
					ret.append(record)
				except:
					continue
		resp = HttpResponse(content_type='application/json')
		resp.content = json.dumps(ret)
		return resp

	else:
		resp = HttpResponse(content_type='application/json', status = 405)
		resp.content = json.dumps({"error" : "send a GET request"})
		return resp