from ast import Not, Return
from audioop import add
from cProfile import Profile
import email
from itertools import permutations, product
from venv import create
from attr import field, validate
from django.http import request, response
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.template import context
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
user = get_user_model()
# from ourcart.ourcart.settings import AUTH_USER_MODEL
from .models import Cart, Product,Category,Banner,CartProduct, UploadFile,User
from .serializers import CartItemSerializer, UserSerializer,Productserializer, CategorySerializer, BannerSerializer,FileSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import make_password



class RegisterView(APIView):
    def post(self, request,format=None):
        serializer = UserSerializer(data=request.data)
        email_exists = User.objects.filter(email=self.request.data['email']).first()
        phone_exist = User.objects.filter(phone=self.request.data['phone']).first()
        if email_exists:
            return Response({"error":True,"message":"email already exist"})
        if phone_exist:
            return Response({"error": True, "message": "phone already exist"})
        data = {}
        if serializer.is_valid():
            account = serializer.save(password=make_password(self.request.data['password']))
            data['error'] = False
            data['message'] = 'registration success'
            data['username'] = account.username
            data['email'] = account.email
            data['phone'] = account.phone
            data['city'] = account.city
            data['userid'] = f'{account.id}'
            token,create=Token.objects.get_or_create(user=account)
            data['token']=token.key
           
        else:
            data['error'] = True
            data['message'] = "email or phone already exist"

        return Response(data)





@csrf_exempt
@api_view(['POST'])
def getToken(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None and password is None:
        return Response({"error": True, "message":"email or password blank"})
    user = authenticate(email=email, password=password)    
    if not user:
        return Response({'error': True,"message":"invalid credentials"})
    token, _ = Token.objects.get_or_create(user=user)
    data = {}
    account=user
    data["error"]=False
    data['message'] = 'login success'
    data["username"]=account.username
    data["email"]=account.email
    data["phone"]=account.phone
    data["city"]=account.city
    data["userid"] = f'{token.user_id}'
    data["token"]=token.key
    return Response(data)






@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_Banner(request):
    banner = Banner.objects.all()
    serializer = BannerSerializer(banner, many=True, context={'request': request})
    if banner.exists():
        return Response({'error': False, 'banners': serializer.data})
    
    return Response({'error': True, 'message': "no datas found"})

        
    
   


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_category(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True, context={'request': request})
    if category.exists():
        return Response({'error': False, 'categories': serializer.data})

    return Response({'error': True, 'message': "no datas found"})

    



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_products(request):
    products = Product.objects.all()
    serializer = Productserializer(products, many=True, context={'request': request})
    if products.exists():
        return Response({'error': False, 'datas': serializer.data})
    return Response({"error":True,"message":"no datas found"})    

    


class ProductDetail(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    def get(self, request):
        product_id = request.data.get("product_id")
        prod = Product.objects.get(id=product_id)
        serializer = Productserializer(prod,context={'request': request})
        if prod !=None:
            return Response({"error": False, "datas": serializer.data})
        else:
            return Response({"error": True, "message": "no datas found"})


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


class AddtoCart(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        product_id = request.data['product_id']
        product_obj = Product.objects.get(id=product_id)
        print("product_obj ",product_obj)
        cart_cart = Cart.objects.filter(user=request.user).filter(complit=False).first()
        print("user ",)
        cart_product_obj = CartProduct.objects.filter(product_id=product_id).first()
        print("cartproduct ",cart_product_obj)
        try:
            if cart_cart:
                # print(cart_cart)
                # print("OLD CART")
                this_product_in_cart = cart_cart.Cartproduct_set.filter(product=cart_product_obj)
                if this_product_in_cart.exists():
                    print("OLD CART PRODUCT--OLD CART")
                    cartprod_uct = CartProduct.objects.filter(product=product_obj).filter(complit=False).first()
                    cartprod_uct.quantity += 1
                    cartprod_uct.subtotal += product_obj.selling_price
                    cartprod_uct.save()
                    cart_cart.total += product_obj.selling_price
                    cart_cart.save()
                else:
                    # print("NEW CART PRODUCT CREATED--OLD CART")
                    cart_product_new = CartProduct.objects.create(
                        cart=cart_cart,
                        price=product_obj.selling_price,
                        quantity=1,
                        subtotal=product_obj.selling_price
                    )
                    cart_product_new.add(product_obj)
                    cart_cart.total += product_obj.selling_price
                    cart_cart.save()
            else:
                # print(cart_cart)
                # print("NEW CART CREATED")
                Cart.objects.create(user=request.user, total=0, complit=False)
                new_cart = Cart.objects.filter(
                    user=request.user).filter(complit=False).first()
                cart_product_new = CartProduct.objects.create(
                    cart=new_cart,
                    price=product_obj.selling_price,
                    quantity=1,
                    subtotal=product_obj.selling_price
                )
                cart_product_new.product.add(product_obj)
                # print("NEW CART PRODUCT CREATED")
                new_cart.total += product_obj.selling_price
                new_cart.save()

            response_mesage = {
                'error': False, 'message': "Product add to card successfully", "productid": product_id}

        except:
            print("error")
            response_mesage = {'error': True,
                               'message': "Product Not add!Somthing is Wromg"}

        return Response(response_mesage)








class FileUpload(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs): 
       file_serializer = FileSerializer(data=request.data)
       if file_serializer.is_valid():
          file_serializer.save()
          return Response({"error": False, "message": "file uploaded successfully"})
       else:
           return Response({"error": True, "message": "file uploaded failed"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_files(request):
    files = UploadFile.objects.all()
    filecount=UploadFile.objects.all().count()
    serializer = FileSerializer(files, many=True, context={'request': request})
    if files.exists():
        return Response({'error': False,"count":str(filecount), 'files': serializer.data})

    return Response({'error': True, 'message': "no datas found"})

class deletefile(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    def post(self,request):
        file_id = request.data.get("file_id")
        if file_id=="":
            return Response({"error": True, "message": "file_id cannot be blank"})
        idexist=UploadFile.objects.filter(id=file_id)
        if idexist:
            item=UploadFile.objects.get(id=file_id)
            item.delete()
            return Response({"error": False, "message": item.fileName + " deleted sucessfully"})    
        else:
            return Response({"error": True, "message":"file_id "+file_id+"  does not exist"})


class fileupdate(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file_id = request.data.get("file_id")
        fileDesc = request.data.get("fileDesc")
        fileName = request.data.get("fileName")
        myfile = request.data.get("myfile")
        if file_id=="":
            return Response({"error": True, "message": "file_id cannot be blank"})
        elif fileDesc=="":
            return Response({"error": True, "message": "fileDesc cannot be blank"})
        elif fileName=="":
            return Response({"error": True, "message": "fileName cannot be blank"})
        elif myfile=="":
            return Response({"error": True, "message": "myfile cannot be blank"})
        idexist=UploadFile.objects.filter(id=file_id)
        if idexist:
            queryset=UploadFile.objects.all()
            files =get_object_or_404(queryset,id=file_id)
            serializer = FileSerializer(files, data=request.data , context={"request": request})
            if serializer.is_valid():
               serializer.save()
               return Response({"error": False, "message": files.fileName + " updated sucessfully"})
            else:
                return Response({"error": True, "message": "something went wrong"})
   
        return Response({"error": True, "message": "file_id  does not exist"})


        
    
                
            
            
                   
            
        









class Catwiseproduct(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    def get(self,request):
        category_id=request.data.get("category_id")
        query=Product.objects.filter(category_id=category_id)
        serializer = Productserializer(query, many=True, context={'request': request})
        if query.exists():
            return Response({"error":False,"datas":serializer.data})
        else:
            return Response({"error":True,"message":"no datas found"})






      


