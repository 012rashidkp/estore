from django.urls import path
from .views import RegisterView, LoginAPIView,Addtocart, ProductDetail, ProductSearch
from . import views


urlpatterns = [
    path('register/', RegisterView.as_view(), name="registerapi"),
    path('login/', LoginAPIView.as_view(), name="loginapi"),
    path('products/', views.get_products, name="products"),
    path('categories/', views.get_category, name="categories"),
    path('banners/', views.get_Banner, name="banners"),
    path('product-search/',ProductSearch.as_view(), name="search"),
    path('product-details/',ProductDetail.as_view(), name="productdetails"),
    path('createcart/', Addtocart.as_view(), name="cart"),


]
