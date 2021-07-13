from ast import Return
from audioop import add
from itertools import product
from venv import create
from attr import validate
from django.http import request
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import exceptions, generics
from rest_framework.authtoken.models import Token
 
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import re
from .models import Cart, Product,Category,Banner,CartProduct
from .serializers import CartItemSerializer, UserSerializer, LoginSerializer ,Productserializer, CategorySerializer, BannerSerializer,CartSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['error'] = False
            data['message'] = 'registration success'
            data['email'] = account.email
            data['phone'] = account.phone
            data['city'] = account.city
            data['username'] = account.username
            data['userid'] = f'{account.id}'
            token,create=Token.objects.get_or_create(user=account)
            data['token']=token.key
           
        else:
            data['error'] = True
            data['message'] = f'{serializer.errors}'

        return Response(data)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data['error'] = False
            data['message'] = 'login success'
            data['username'] = user.username
            data['email'] = user.email
            data['phone'] = user.phone
            data['city'] = user.city
            data['userid'] = f'{token.user_id}'
            data['token'] = token.key
        else:
            data['error'] = True
            data['message'] = f'{serializer.errors}'
        return Response(data)





@api_view(['GET'])
def get_Banner(request):
    banner = Banner.objects.all()
    serializer = BannerSerializer(
        banner, many=True, context={'request': request})
    return Response({'error': False, 'banners': serializer.data})



@api_view(['GET'])
def get_category(request):
    category = Category.objects.all()
    serializer = CategorySerializer(
        category, many=True, context={'request': request})
    return Response({'error': False, 'categories': serializer.data})



@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = Productserializer(
        products, many=True, context={'request': request})
    return Response({'error': False, 'datas': serializer.data})


class ProductDetail(APIView):
    serializer_class = Productserializer

    def get(self, request, *args, **kwargs):
        try:
            id = request.query_params["id"]
            if id != None:
                item = Product.objects.get(id=id)
                serializer = Productserializer(
                    item, context={'request': request})
                response = {
                    "error": False,
                    "data": serializer.data
                }
        except:
            response = {
                "error": True,
                "message": "datas not available"
            }

        return Response(response)


class setpagination(PageNumberPagination):
    page_size = 4


class Pagination(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    pagination_class = setpagination
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('title')


class ProductSearch(APIView):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filter_fields = ('title',)


class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user:
                cart_obj.user = request.user
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


class Addtocart(APIView):
    def post(self,request,*args,**kwargs):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            serializer.save()
            return Response({"error":False,"message":"cart addedd successfully"})

        else:
            return Response({"error":True,"message":"failed"})    

   







      


