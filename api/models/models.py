from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def create_auth_token(sender, instance=None, created=False, **kwargs):
#    if created:
#        Token.objects.create(user=instance)
#    for user in User.objects.all():
#    	Token.objects.get_or_create(user=user)

class Article(models.Model):
	#id = models.IntegerField(primary_key = True)
	reddit_id = models.CharField(max_length = 200,unique=True)
	permalink = models.CharField(max_length = 2000)
	url = models.CharField(max_length = 2000)
	author = models.CharField(max_length = 500)
	class Meta:
		db_table = 'article'

class Favorite(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	reddit_id = models.CharField(max_length = 200)
	class Meta:
		db_table = 'favorite'

class Tags(models.Model):
	favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
	tag = models.CharField(max_length = 2000)
	class Meta:
		db_table = 'tags'