from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.db import connections
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http.response import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.utils.encoding import smart_str
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D

import base64
import io
import sys
import os
import json 
# from pandas import read_sql,DataFrame,to_numeric
import secrets
from time import sleep,time
from datetime import datetime,timedelta
import logging
import requests as rqs
from blogs.models import *

'''
login fucntion to check if email pass exists in our database. If yes then give a token
to be later used for further api calls
'''
@csrf_exempt
def login(request):
  if request.method=='POST' or request.method=='GET':
    email=request.GET.get('email', 'NoEmail')
    password=request.GET.get('password', 'NoPassword')
    #Check if email pass is entered
    if email=='No' or password=='No':
      return JsonResponse({'success':False,
                  "Status":'Field cannot be empty'})
    #Search for the user
    user_=User.objects.filter(
              email=email,
              password=password).first()
    try:
      if user_.email:
        #Check if token already exists
        token_ = Token.objects.filter(email=email,password=password).first()
        try:
          if token_.token:
            return JsonResponse({'success':True,
              "Status":"Toekn Already created",
              "Token":token_.token})
        except Exception as e:
          #Create a token using secrets
          token=secrets.token_hex(10)
          #Create the token record in the database
          token_ = Token.objects.create(token=token,
            email=email,password=password)
          return JsonResponse({'success':True,
            "Status":"Token created sucessfully",
            "Token":token})
    except Exception as e:
      return JsonResponse({'success':False,
                  "Status":'User doenst exist in our database'})

'''
category and tag functions are used to post a category and tag respectively
NOTE: Every tag is associated with a blog so slug is required for both
'''
@csrf_exempt
def category(request):
  token=request.GET.get('token', 'No')
  token_=Token.objects.filter(
              token=token).first()
  try:
    if token_.token:
      pass
  except:
    return JsonResponse({'success':False,
        "Status":"Token doesnt exist"})
  if request.method=='POST':
    category_name=request.GET.get('category_name', 'NoName')
    slug=request.GET.get('slug', 'NoSlug')
    #Check if catergory name and sluf is entered or not
    if category_name=='NoName' or slug=='NoSlug':
      return JsonResponse({'success':False,
        "Status":"Please Enter category_name and slug"})
    #Get or Create Category from the Category model
    cat = Category.objects.get_or_create(category_name=category_name,
              slug=slug)
    return JsonResponse({'success':True,
                "Status":"POST succesful"})
  else:
    return JsonResponse({'success':False,
        "Status":"Please Use POST method"})

@csrf_exempt
def tag(request):
  token=request.GET.get('token', 'No')
  token_=Token.objects.filter(
              token=token).first()
  try:
    if token_.token:
      pass
  except:
    return JsonResponse({'success':False,
        "Status":"Token doesnt exist"})
  if request.method=='POST':
    tag_name=request.GET.get('tag_name', 'NoName')
    slug=request.GET.get('slug', 'NoSlug')
    #Check if tag name and sluf is entered or not
    if tag_name=='NoName' or slug=='NoSlug':
      return JsonResponse({'success':False,
        "Status":"Please Enter tag_name and slug"})
    #Get or Create Tag from the Tag model
    tag = Tag.objects.get_or_create(tag_name=tag_name,
              slug=slug)
    return JsonResponse({'success':True,
                "Status":"POST succesful"})
  else:
    return JsonResponse({'success':False,
        "Status":"Please Use POST method"})

'''
blog function is used to CRUD a blog post
'''
@csrf_exempt
def blog(request):
  token=request.GET.get('token', 'No')
  token_=Token.objects.filter(
              token=token).first()
  try:
    if token_.token:
      pass
  except:
    return JsonResponse({'success':False,
        "Status":"Token doesnt exist"})
  if request.method=='POST':
    tags_names=request.GET.getlist('tags_names', 'NoTags')
    category_name=request.GET.getlist('category_name', 'NoCategories')
    slug=request.GET.get('slug', 'NoSlug')
    #check for slug if not generate a new value
    if slug=='NoSlug':
      slug=secrets.token_hex(10)
    title=request.GET.get('title', 'NoTitle')
    # search for user with email and password 
    user_= User.objects.filter(email=token_.email,
              password=token_.password).first()
    author_name=user_.name
    # search for blog with thte slug title and author name(i.e. users name)
    blog_=Blog.objects.filter(
              slug=slug,
              title=title,
              author_name=author_name).first()
    #check if blog is there, if yes then return blog exists error
    try:
      if blog_.slug:
        return JsonResponse({'success':False,
          "Status":"Blog title already exists use PUT to Update"})
    except:
      pass
    # loop between all the tags and categories and store them with the slug of the blog in 
    # their respective tables.
    for i,j in zip(tags_names,category_name):
      tag=Tag.objects.get_or_create(tag_name=i,slug=slug)
      cat=Category.objects.get_or_create(category_name=j, slug=slug)
      blog_=Blog.objects.get_or_create(
              category_name=cat[0],
              tags_names=tag[0],
              slug=slug,
              title=title,
              author_name=author_name)
    return JsonResponse({'success':True,
                "Status":"Posted succesfully"})
  elif request.method=='GET':
    title=request.GET.get('title', 'NoTitle')
    # search for user with email and password 
    user_= User.objects.filter(email=token_.email,
              password=token_.password).first()
    author_name=user_.name
    # search for blog with thte slug title and author name(i.e. users name)
    blog_=Blog.objects.filter(
                  title=title,
                  author_name=author_name).first()
    # check if blog exists, if yes then collect all tags and categories of the 
    # blog from their respective tables and return the whole info
    try:
      if blog_.slug:
        category_names=Category.objects.filter(slug=blog_.slug).all()
        category_names=[x.category_name for x in category_names]
        tags_names=Tag.objects.filter(slug=blog_.slug).all()
        tags_names=[x.tag_name for x in tags_names]
        return JsonResponse({'success':True,
                  "Status":"Queried succesfully",
                  "title":blog_.title,
                  "slug":blog_.slug,
                  "author_name":blog_.author_name,
                  "category_name":category_names,
                  "tags_names":tags_names})
    except:
      return JsonResponse({'success':False,
                "Status":"Blog Title Doesnt exist"})
  elif request.method=='PUT':
    tags_names=request.GET.getlist('tags_names', 'NoTags')
    category_name=request.GET.getlist('category_name', 'NoCategories')
    title=request.GET.get('title', 'NoTitle')
    # search for user with email and password 
    user_= User.objects.filter(email=token_.email,
              password=token_.password).first()
    author_name=user_.name
    #loop with all the tags and categories and update the blog data along with the category
    # and tag associated to that particular blog
    for i,j in zip(tags_names,category_name):
      tag=Tag.objects.get_or_create(tag_name=i,slug=slug)
      cat=Category.objects.get_or_create(category_name=j, slug=slug)
      blog_=Blog.objects.filter(
              category_name=cat[0],
              tags_names=tag[0],
              title=title,
              author_name=author_name).update(
              category_name=cat[0],
              tags_names=tag[0],
              title=title,
              author_name=author_name)
    return JsonResponse({'success':True,
                "Status":"Updated succesfully"})
  elif request.method=='DELETE':
    title=request.GET.get('title', 'NoTitle')
    # search for user with email and password 
    user_= User.objects.filter(email=token_.email,
          password=token_.password).first()
    author_name=user_.name
    # search for blog with thte slug title and author name(i.e. users name)
    blog_=Blog.objects.filter(
              title=title,
              author_name=author_name).first()
    # search for all the tags and categories associated to that blog 
    # and loop betwwen them and delete every instance.
    category_names=Category.objects.filter(slug=blog_.slug).all()
    category_names=[x.category_name for x in category_names]
    tags_names=Tag.objects.filter(slug=blog_.slug).all()
    tags_names=[x.tag_name for x in tags_names]
    for i,j in zip(tags_names,category_names):
      tag=Tag.objects.filter(tag_name=i,slug=blog_.slug).delete()
      cat=Category.objects.filter(category_name=j, slug=blog_.slug).delete()
    blog_=blog_.delete()
    return JsonResponse({'success':True,
                "Status":"Deleted succesfully"})

@csrf_exempt
def user(request):
  if request.method=='POST' or request.method=='PUT':
    email=request.GET.get('email', 'No')
    password=request.GET.get('password', 'No')
    name=request.GET.get('name', 'No')
    address=request.GET.get('address', 'No')
    # check if any of the info is not passed
    if email=='No' or password=='No' or name=='No' or address=='No':
      return JsonResponse({'success':False,
                  "Status":'Field cannot be empty'})
    # use position stack('cuz of 25000 free calls') to geocode the given address and use 
    # 1.1 and 2.2 if it cannot geocode it
    js=rqs.get(f"http://api.positionstack.com/v1/forward?access_key={settings.POSITIONSTACK_KEY}&query={address}")
    try:
      js=js.json()
      latitude=js['data'][0]['latitude']
      longitude=js['data'][0]['longitude']
    except:
      latitude=1.1
      longitude=2.2
    # create a record of the user in the database, Using GIS class Point to convert the lat
    # lon to a POint
    user_ = User.objects.get_or_create(email=email,
              password=password,
              name=name,
              address=address,
              lon=longitude,
              lat=latitude,
              point=Point(x=longitude, y=latitude, srid=4326))
    if user_[1]:
      return JsonResponse({'success':True,
                  "Status":'Created succesfully'})
    else:
      return JsonResponse({'success':True,
                "Status":"Email/Pass Already exists so Updated"})
  elif request.method=='GET':
    email=request.GET.get('email', 'NoEmail')
    password=request.GET.get('password', 'NoPassword')
    name=request.GET.get('name', 'NoName')
    address=request.GET.get('address', 'NoAddress')
    # use position stack('cuz of 25000 free calls') to geocode the given address and use 
    # 1.1 and 2.2 if it cannot geocode it
    js=rqs.get(f"http://api.positionstack.com/v1/forward?access_key={settings.POSITIONSTACK_KEY}&query={address}")
    try:
      js=js.json()
      latitude=js['data'][0]['latitude']
      longitude=js['data'][0]['longitude']
    except:
      latitude=1.1
      longitude=2.2
      return JsonResponse({'success':False,
                "Status":"Couldnt convert address to lat lon, pLease provide proper address"})
    # Create a point using GEOSGeometry with crs 4326
    pnt = GEOSGeometry(f'POINT({longitude} {latitude})', srid=4326)
    # search for all the users withtin 1 km distance
    qs = User.objects.filter(point__distance_lte=(pnt, D(km=1)))
    # collect only the name of the user
    users=[x.name for x in qs]
    return JsonResponse({'success':True,
                "Users in 1 km radius":users,
                "Status":"Queried succesfully"})
  elif request.method=='DELETE':
    email=request.GET.get('email', 'NoEmail')
    password=request.GET.get('password', 'NoPassword')
    name=request.GET.get('name', 'NoName')
    address=request.GET.get('address', 'NoAddress')
    user_ = User.objects.filter(email=email,
                  password=password,
                  name=name,
                  address=address).delete()
    return JsonResponse({'success':True,
                    "Status":"Deleted succesfully"})

@csrf_exempt
def comment(request):
  token=request.GET.get('token', 'No')
  token_=Token.objects.filter(
              token=token).first()
  try:
    if token_.token:
      pass
  except:
    return JsonResponse({'success':False,
        "Status":"Token doesnt exist"})
  if request.method=='POST':
    user__=User.objects.filter(email=token_.email,
              password=token_.password)
    user_= user__.first()
    email=user_.email
    password=user_.password
    title=request.GET.get('title', 'NoName')
    author_name=user_.name
    comment=request.GET.get('comment', 'NoName')
    # seach for the user using the email and pass
    user_= User.objects.filter(email=email,
              password=password).first()
    #Search for blog
    blog_=Blog.objects.filter(
              title=title,
              author_name=author_name).first()
    #check if the blog exists or not
    try:
      if blog_.slug:
        pass
    except:
      return JsonResponse({'success':False,
          "Status":"Blog title doesnt exists"})
    # create a comment recvord
    comment_=Comment.objects.get_or_create(blog=blog_,
              user=user_,
              comment=comment)
    return JsonResponse({'success':True,
                "Status":"Created succesfully"})
  elif request.method=='DELETE':
    user__=User.objects.filter(email=token_.email,
              password=token_.password)
    user_= user__.first()
    email=user_.email
    password=user_.password
    title=request.GET.get('title', 'NoName')
    author_name=user_.name
    comment=request.GET.get('comment', 'NoName')

    blog_=Blog.objects.filter(
              title=title,
              author_name=author_name).first()
    comment_=Comment.objects.filter(blog=blog_,
              user=user_,
              comment=comment).delete()
    return JsonResponse({'success':True,
                "Status":"Deleted succesfully"})

@csrf_exempt
def content(request):
  token=request.GET.get('token', 'No')
  token_=Token.objects.filter(
              token=token).first()
  try:
    if token_.token:
      pass
  except:
    return JsonResponse({'success':False,
        "Status":"Token doesnt exist"})
  if request.method=='GET' or request.method=='POST':
    user__=User.objects.filter(email=token_.email,
              password=token_.password)
    user_= user__.first()
    email=user_.email
    password=user_.password
    content=request.GET.get('content', 'NoEmail')
    date_creation=datetime.now()
    title=request.GET.get('title', 'NoName')
    slug=request.GET.get('slug', 'NoSlug')
    # if slug is passed use it else use the title only
    if slug=='NoSlug':
      blog_=Blog.objects.filter(
              title=title).first()
    else:
      blog_=Blog.objects.filter(
              title=title,
              slug=slug).first()
    # check if blog title exists or not
    try:
      if blog_.slug:
        pass
    except:
      return JsonResponse({'success':False,
          "Status":"Blog title doesnt exists"})
    # search for categories nad tags associated to that blog
    category_names=Category.objects.filter(slug=blog_.slug).values()
    tags_names=Tag.objects.filter(slug=blog_.slug).values()

    auth=user_.name
    comment_=Comment.objects.filter(blog=blog_)
    comments__=comment_.values()
    # count the number of comments for the blofg
    comments_count=comment_.count()
    # count for the number of comments in the blog assocaited to the given user
    is_user_comment_inside=Comment.objects.filter(blog=blog_,user=user_).count()
    if is_user_comment_inside>0:
      is_user_comment_inside=True
    else:
      is_user_comment_inside=False
    if request.method=='POST':
      content_=Content.objects.get_or_create(blog=blog_,
                user=user_,
                comments_count=comments_count,
                category=blog_.category_name,
                tag=blog_.tags_names)
    user=list(user__.values())[0]
    user.pop('point')
    return JsonResponse({'success':True,
      "content":content,
      "category_names":list(category_names),
      "tags_names":list(tags_names),
      "comments":list(comments__),
      "user":user
      })



