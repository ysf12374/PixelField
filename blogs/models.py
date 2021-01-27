from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

class Token(models.Model):
	email = models.CharField('email', max_length=50, null=True)
	password = models.CharField('password', max_length=50, null=True)
	token = models.CharField('Token', max_length=120)
	date_creation = models.DateTimeField('Date Creation',default=datetime.now)
	id = models.AutoField(primary_key=True)

class Category(models.Model):
	category_name = models.CharField('category name', max_length=120)
	slug = models.CharField('slug',max_length=120)
	id = models.AutoField(primary_key=True)

class Tag(models.Model):
	tag_name = models.CharField('tag name', max_length=120)
	slug = models.CharField('slug',max_length=120)
	id = models.AutoField(primary_key=True)

class Blog(models.Model):
	title = models.CharField('title', max_length=240)
	slug = models.CharField('slug',max_length=240)
	author_name = models.CharField(max_length=120)
	category_name = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,
    null=True)
	tags_names = models.ForeignKey(Tag, on_delete=models.CASCADE,blank=True,
    null=True)
	

class User(models.Model):
    email = models.CharField('email',max_length=50)
    password = models.CharField('password',max_length=50)
    name = models.CharField('name',max_length=50)
    address = models.CharField('address',max_length=50,blank=True, null=True)
    lon = models.FloatField()
    lat = models.FloatField()
    point = models.PointField()

class Comment(models.Model):
	blog=models.ForeignKey(Blog, on_delete=models.CASCADE,blank=True,
    null=True)
	comment = models.CharField('comment', max_length=250)
	user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,
    null=True)

class Content(models.Model):
	content = models.CharField('content', max_length=1440)
	date_creation = models.DateTimeField('Date Creation',default=datetime.now)
	comments_count = models.IntegerField(default=0)
	is_user_comment_inside = models.BooleanField(default=False)
	blog=models.ForeignKey(Blog, on_delete=models.CASCADE,blank=True,
    null=True)
	user=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,
    null=True)
	comment=models.ForeignKey(Comment, on_delete=models.CASCADE,blank=True,
    null=True)
	category=models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,
    null=True)
	tag=models.ForeignKey(Tag, on_delete=models.CASCADE,blank=True,
    null=True)


