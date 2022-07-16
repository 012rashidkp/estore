from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message
from .models import Cart, Product, Category, Banner, CartProduct, UploadFile, User
from .serializers import CartItemSerializer, UserSerializer, Productserializer, CategorySerializer, BannerSerializer, FileSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from audioop import add
from venv import create
from attr import field, validate
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.template import context
from grpc import Status
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import exceptions, generics
from rest_framework.authtoken.models import Token
from rest_framework import views
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import re
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
User = get_user_model()
# from ourcart.ourcart.settings import AUTH_USER_MODEL

class RegisterView(APIView):

    def post(self, request):
        data = {}
        username = request.data.get('username', False)
        email = request.data.get('email', False)
        city = request.data.get('city', False)
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        if not username:
            data["error"] = True
            data["message"] = "username is required"
        elif not email:
            data["error"] = True
            data["message"] = "email is required"
        elif not city:
            data["error"] = True
            data["message"] = "city is required"
        elif not phone:
            data["error"] = True
            data["message"] = "phone is required"
        elif not password:
            data["error"] = True
            data["message"] = "password is required"
        else:
            email_exists = User.objects.filter(email=self.request.data['email']).first()
            phone_exist = User.objects.filter(phone=self.request.data['phone']).first()
            if email_exists:
                data["error"] = True
                data["message"] = "email already exist"
            if phone_exist:
                data["error"] = True
                data["message"] = "phone already exist"
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save(
                password=make_password(self.request.data['password']))
            data['error'] = False
            data["status_code"] = f'{status.HTTP_201_CREATED}'
            data['message'] = 'registration success'
            data["created_at"] = account.created_at
            data['username'] = account.username
            data['email'] = account.email
            data['phone'] = account.phone
            data['city'] = account.city
            data['userid'] = f'{account.id}'
            token, create = Token.objects.get_or_create(user=account)
            data['token'] = token.key
        return Response(data)


class Sendnotification(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    def post(self,request):
        data={}
        title = request.data.get('title',False)
        body = request.data.get('body',False)
        registration_id=
        
        
        
        






@csrf_exempt
@api_view(['POST'])
def getToken(request):
    data = {}
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None and password is None:
        data["error"]=True
        data["message"] = "email or password blank"
    emailexist = User.objects.filter(email=email).exists()
    if not emailexist:
        data["error"]=True
        data["message"] = "wrong email"
    else:
        user = authenticate(email=email, password=password)
        if not user:
            data["error"]=True
            data["message"] = "wrong paswword"
        else:
            token, _ = Token.objects.get_or_create(user=user)

            account = user
            data["error"] = False
            data["status_code"] = f'{status.HTTP_201_CREATED}'
            data['message'] = 'login success'
            data['created_at'] = account.created_at
            data["username"] = account.username
            data["email"] = account.email
            data["phone"] = account.phone
            data["city"] = account.city
            data["userid"] = f'{token.user_id}'
            data["token"] = token.key
    return Response(data)


@api_view(['POST'])
def getSuperuser(request):
    data = {}
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None and password is None:
        data["error"] = True
        data["message"] = "email or password blank"
    emailexist = User.objects.filter(email=email).exists()
    if not emailexist:
        data["error"] = True
        data["message"] = "wrong email"
    else:
        user = authenticate(email=email, password=password)
        if not user:
            data["error"] = True
            data["message"] = "wrong paswword"
        elif not user.is_superuser:
            data["error"] = True
            data["message"] = "you are not a admin"
        else:
            token, _ = Token.objects.get_or_create(user=user)
            account = user
            data["error"] = False
            data["status_code"] = f'{status.HTTP_201_CREATED}'
            data['message'] = 'login success you are a admin'
            data['created_at'] = account.created_at
            data["username"] = account.username
            data["email"] = account.email
            data["phone"] = account.phone
            data["city"] = account.city
            data["userid"] = f'{token.user_id}'
            data["token"] = token.key
    return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_Banners(request):
    banner = Banner.objects.all()
    serializer = BannerSerializer(
        banner, many=True, context={'request': request})
    if banner.exists():
        return Response({'error': False, 'banners': serializer.data})

    return Response({'error': True, 'message': "no datas found"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_categories(request):
    category = Category.objects.all()
    serializer = CategorySerializer(
        category, many=True, context={'request': request})
    data = {}
    if category.exists():
        data["error"] = False
        data["categories"] = serializer.data
    else:
        data["error"] = True
        data["message"] = "no datas found"
    return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_products(request):
    products = Product.objects.all()
    serializer = Productserializer(
        products, many=True, context={'request': request})
    data = {}
    if products.exists():
        data["error"] = False
        data["datas"] = serializer.data
    else:
        data["error"] = True
        data["message"] = "no datas found"
    return Response(data)


class ProductDetail(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        product_id = request.data.get("product_id")
        spec_prod = Product.objects.get(id=product_id)
        serializer = Productserializer(spec_prod, context={'request': request})
        data = {}
        if spec_prod != None:
            data["error"] = False
            data["datas"] = serializer.data
        else:
            data["error"] = True
            data["message"] = "no datas found"
        return Response(data)


class setpagination(PageNumberPagination):
    page_size = 4


class Pagination(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    pagination_class = setpagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title')


class ProductSearch(APIView):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filter_fields = ('title',)


class AddtoCart(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request, format=None):
        product_id = request.POST.get('product_id', None)
        if product_id is not None:
            try:
                product_obj = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                pass
            cart_instance, created = Cart.objects.new_or_get(request)
            if product_obj in cart_instance.items.all():
                cart_instance.items.remove(product_obj)
                added = False
            else:
                cart_instance.items.add(product_obj)
                added = True
            data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_instance.items.count()
            }
            return Response(data)


class FileUpload(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        data = {}
        if file_serializer.is_valid():
            file_serializer.save()
            data["error"] = False
            data["message"] = "file uploaded successfully"
        else:
            data["error"] = True
            data["message"] = "file uploaded failed"
        return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_files(request):
    files = UploadFile.objects.all()
    filecount = UploadFile.objects.all().count()
    serializer = FileSerializer(files, many=True, context={'request': request})
    data = {}
    if files.exists():
        data["error"] = False
        data["count"] = str(filecount)
        data["files"] = serializer.data
    else:
        data["error"] = True
        data["message"] = "no datas found"
    return Response(data)


class deletefile(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        file_id = request.data.get("file_id")
        data = {}
        if file_id is None:
            data["error"] = True
            data["message"] = "please place required parameter"
        elif file_id == "":
            data["error"] = True
            data["message"] = "file_id cannot be blank"
        idexist = UploadFile.objects.filter(id=file_id)
        if idexist:
            item = UploadFile.objects.get(id=file_id)
            item.delete()
            data["error"] = False
            data["message"] = item.fileName + "  deleted sucessfully"
        else:
            data["error"] = True
            data["message"] = f'{file_id}'+" file_id does not exist"
        return Response(data)


class fileupdate(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_id = request.data.get("file_id")
        fileDesc = request.data.get("fileDesc")
        fileName = request.data.get("fileName")
        myfile = request.data.get("myfile")
        data = {}
        if file_id or fileDesc or fileName or myfile is None:
            data["error"] = True
            data["message"] = "required parameters cannot be blank"
        if file_id == "":
            data["error"] = True
            data["message"] = "file_id cannot be blank"
        elif fileDesc == "":
            data["error"] = True
            data["message"] = "fileDesc cannot be blank"
        elif fileName == "":
            data["error"] = True
            data["message"] = "fileName cannot be blank"
        elif myfile == "":
            data["error"] = True
            data["message"] = "myfile cannot be blank"
        idexist = UploadFile.objects.filter(id=file_id)
        if idexist:
            queryset = UploadFile.objects.all()
            files = get_object_or_404(queryset, id=file_id)
            serializer = FileSerializer(
                files, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                data["error"] = False
                data["message"] = files.fileName + " updated sucessfully"
            else:
                data["error"] = True
                data["message"] = "something went wrong"
        return Response(data)


class Catwiseproduct(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        category_id = request.data.get("category_id")
        query = Product.objects.filter(category_id=category_id)
        serializer = Productserializer(
            query, many=True, context={'request': request})
        data = {}
        if category_id is None:
            data["error"] = True
            data["message"] = "please place required parameter"
        elif category_id == None:
            data["error"] = True
            data["message"] = "category_id cannot be blank"
        elif query.exists():
            data["error"] = False
            data["datas"] = serializer.data
        else:
            data["error"] = True
            data["message"] = "no datas found"
        return Response(data)
