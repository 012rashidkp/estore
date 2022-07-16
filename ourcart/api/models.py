import email
from statistics import mode
from unicodedata import name
from django.db import models

# Create your custom user model.
from django.contrib.auth.models import  BaseUserManager,AbstractBaseUser

from django.db import models
#from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



# class CustomUserManager(BaseUserManager):
#     """Define a model manager for User model with no username field."""

#     def _create_user(self, email, password=None, **extra_fields):
#         """Create and save a User with the given email and password."""
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)

#     def create_superuser(self, email, password=None, **extra_fields):
#         """Create and save a SuperUser with the given email and password."""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self._create_user(email, password, **extra_fields)


# class User(AbstractUser):
#     username = None
#     first_name = None
#     last_name = None
#     email = models.EmailField(_('email address'), unique=True)
#     username = models.CharField(max_length=150)
#     phone = models.CharField(max_length=10)
#     city = models.CharField(max_length=150)
#     USERNAME_FIELD = 'email'
#     FIRSTNAME_FIELD = 'username'
#     LASTNAME_FIELD = 'phone'
#     EXTRA_FIELD = 'city'

#     REQUIRED_FIELDS = ['username', 'phone', 'city']

#     objects = CustomUserManager()
    
    

# product related models


class MyAccountManager(BaseUserManager):
    def create_user(self, email, phone=None,created_at=None, city=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=self.normalize_email(email),city=city)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=self.normalize_email(email),password=password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email", max_length=60, unique=True, blank=True, null=True, default=None)
    city = models.CharField(max_length=30, blank=True, null=True, default=None)
    phone = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField( max_length=30,blank=True, null=True)
    created_at=models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_super_teacher = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    class Meta:
        db_table = "authusers"

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser






class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins/")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Banner(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="banners/")
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = "Banners"


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="categories/")

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Categories"

class Product(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True)
    return_policy = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Products"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    images = models.ImageField(upload_to="Productimages/")

    @property
    def image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.images.url)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Products_Images"

COLORS = (
    ("no colors", "no colors"),
    ("Red", "Red"),
    ("Green", "Green"),
    ("Yellow", "Yellow"),
    ("Pink", "Pink"),
    ("Brown", "Brown"),
    ("Black", "Black"),
    ("White", "White"),
)


class ProductColor(models.Model):
    Product = models.ForeignKey(
        Product, related_name='colors', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    colors = models.CharField(
        choices=COLORS, max_length=20, default="no colors")

    def __str__(self):
        return self.colors
    
    class Meta:
        db_table = "Products_Colors"


SIZES = (
    ("no sizes", "no sizes"),
    ("uk=4", "uk-4"),
    ("uk-5", "uk-5"),
    ("uk-6", "uk-6"),
    ("uk-7", "uk-7"),
    ("uk-8", "uk-8"),
    ("uk-9", "uk-9"),
    ("uk-10", "uk-10"),

)


class ProductSize(models.Model):
    Product = models.ForeignKey(Product, related_name='sizes',
                                on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    sizes = models.CharField(choices=SIZES, max_length=100, default='no sizes')

    def __str__(self):
        return self.sizes
    
    class Meta:
        db_table = "Products_Sizes"


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    complit = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    is_in_order = models.BooleanField(default=False)

    def __str__(self):
        return "Cart: " + str(self.id)
    
    class Meta:
        db_table = "Cart"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, default="no_color", on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, default="no_sizes", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_charge = models.PositiveBigIntegerField(default=100)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Cart=={self.cart.id}<==>CartProduct:{self.id}==Qualtity=={self.quantity}"
    
    class Meta:
        db_table = "Cart_Items"


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=55)
    city = models.CharField(max_length=55)
    pincode = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    destinationtype = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Shipping_Address"


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti"),
    ("Esewa", "Esewa"),
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=False)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)
    
    class Meta:
        db_table = "Product_Orders"


class UploadFile(models.Model):
    fileName = models.CharField(max_length=150, blank=False, null=False)
    fileDesc = models.CharField(max_length=150, blank=False, null=False)
    myfile = models.FileField(upload_to="uploads/")
    date = models.DateField(auto_now=True)
    
    class Meta:
        db_table = "Uploads"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)









