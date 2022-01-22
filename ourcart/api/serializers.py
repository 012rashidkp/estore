
from email.policy import default
from api.models import Cart
from asyncore import write
from itertools import product
from turtle import color

from django.http import request
from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
User = get_user_model()
from .models import Product,Category,Banner,ProductImage,ProductColor,ProductSize,CartProduct,UploadFile

class UserSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(source='id', read_only=True)
    password = serializers.CharField(max_length=65, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=15, min_length=4),
    city = serializers.CharField(max_length=100, min_length=2)
    phone = serializers.CharField(max_length=10, min_length=2)
    username = serializers.CharField(max_length=150, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'city', 'email', 'password', 'phone', 'userid']

    





class BannerSerializer(serializers.ModelSerializer):
    banner_id = serializers.CharField(source='id')
    banner_name = serializers.CharField(source='title')
    banner_image=serializers.ImageField(source='image')
    class Meta:
        model = Banner
        fields=('banner_id','banner_name','banner_image')

class CategorySerializer(serializers.ModelSerializer):
    cat_id = serializers.CharField(source='id')
    cat_name = serializers.CharField(source='title')
    cat_image = serializers.ImageField(source='image')

    class Meta:
        model = Category
        fields =('cat_id','cat_name','cat_image')

class prodimageserializer(serializers.ModelSerializer):
    imageID=serializers.CharField(source="id",read_only=True)
    prodimages=serializers.ImageField(source="images",read_only=True)
    prodName=serializers.CharField(source="name",read_only=True)
    product_ID = serializers.CharField(source="product_id", read_only=True)
    
    class Meta:
        model=ProductImage
        fields = ('imageID', 'prodimages', 'prodName', 'product_ID')


class ProdColorSerializer(serializers.ModelSerializer):
    colorID=serializers.CharField(source="id",read_only=True)
    prodcolors = serializers.CharField(source="colors", read_only=True)
    prodName=serializers.CharField(source="name",read_only=True)
    product_ID = serializers.CharField(source="product_id", read_only=True)
    class Meta:
        model=ProductColor
        fields = ("colorID", "prodcolors", "prodName", "product_ID")

class prodSizeSerializer(serializers.ModelSerializer):
    sizeID=serializers.CharField(source="id",read_only=True)
    prodsizes = serializers.CharField(source="sizes", read_only=True)
    prodName=serializers.CharField(source="name",read_only=True)
    product_ID = serializers.CharField(source="product_id", read_only=True)
    class Meta:
        model=ProductSize
        fields = ("sizeID", "prodsizes", "prodName", "product_ID")
      

class Productserializer(serializers.ModelSerializer):
    
    category_name = serializers.CharField(source='category')
    cat_id = serializers.CharField(source='category_id')
    prod_id = serializers.CharField(source='id')
    prodimages = prodimageserializer(source="images",many=True,read_only=True)
    prodcolors = ProdColorSerializer(source="colors",many=True,read_only=True)
    prodsizes = prodSizeSerializer(source="sizes",many=True,read_only=True,allow_null=False)
    
    class Meta:
        model = Product
        fields = ('prod_id', 'title', 'image', 'marked_price', 'selling_price', 'description', 
                  'warranty', 'return_policy', 'category_name', 'cat_id', 'prodimages', 'prodcolors', 'prodsizes')
        
        

    
class CartSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField(source='User.id',write_only=True)
    user_id = serializers.IntegerField(source='user.id',read_only=True)
  

    class Meta:
        model = Cart
        fields = ( 'user_id',)


class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(required=True)
    product_id = serializers.IntegerField(source='product.id')
    color_id = serializers.IntegerField(source='ProductColor.id')
    size_id = serializers.IntegerField(source='ProductSize.id')
   

    class Meta:
        model = CartProduct
        fields = ('cart', 'product_id', 'color_id', 'size_id')

    def create(self, validated_data):
        cart_data = validated_data.pop('cart')
        cart= CartSerializer.create(
            CartSerializer(), validated_data=cart_data)

        proditem, created = CartProduct.objects.update_or_create(cart=cart,
            product_id=validated_data.pop('product_id'),
            color_id=validated_data.pop('color_id'), size_id=validated_data.pop('size_id'))

        return proditem


class FileSerializer(serializers.ModelSerializer):
    file_id = serializers.CharField(source='id',read_only=True)
    class Meta:
        model = UploadFile
        fields = ('file_id','fileName', 'fileDesc', 'myfile')


   
    
       


 
    
   
    
