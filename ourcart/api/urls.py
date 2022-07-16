from django.urls import path
from .views import RegisterView,AddtoCart, ProductDetail, ProductSearch,FileUpload,deletefile, get_files
from . import views

""" EndPoints Api """

urlpatterns = [
    path('register/', RegisterView.as_view(), name="registerapi"),
    path('products/', views.get_products, name="products"),
    path('categories/', views.get_categories, name="categories"),
    path('banners/', views.get_Banners, name="banners"),
    path('product-search/',ProductSearch.as_view(), name="search"),
    path('product-details/',ProductDetail.as_view(), name="productdetails"),
    path('addtocart/', AddtoCart.as_view(), name="addtocart"),
    path('login/', views.getToken, name='getauthtoken'),
    path('superuserlogin/', views.getSuperuser, name='getsuperuser'),
    path('fileupload/',FileUpload.as_view(),name="upload"),
    path('getfiles/', views.get_files,name="getfiles"),
    path('catwiseproduct/',views.Catwiseproduct.as_view(),name="catwise"),
    path('deletefile/',deletefile.as_view(),name="deletefile"),
    path('updatefile/', views.fileupdate.as_view(),name="updatefile")
    
]
