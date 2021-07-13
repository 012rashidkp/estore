from django.db import models
from django.conf import settings

# Create your custom user model.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth import get_user_model
# User = get_user_model()

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150)
    phone = models.CharField(max_length=10)
    city = models.CharField(max_length=150)
    USERNAME_FIELD = 'email'
    FIRSTNAME_FIELD = 'username'
    LASTNAME_FIELD = 'phone'
    EXTRA_FIELD = 'city'

    REQUIRED_FIELDS = ['username', 'phone', 'city']

    objects = CustomUserManager()


#product related models

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Banner(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="banners")

    def __str__(self):
        return self.title



class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="categories")
    def __str__(self):
        return self.title







class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True)
    return_policy = models.CharField(max_length=300, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=100)    
    images = models.ImageField(upload_to="Productimages")

    @property
    def image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.images.url)
    def __str__(self):
        return self.name


COLORS = (
    ("no colors","no colors"), 
    ("Red","Red"), 
    ("Green","Green"),
    ("Yellow","Yellow"), 
    ("Pink","Pink"), 
    ("Brown","Brown"), 
    ("Black","Black"), 
    ("White","White"),
    )


class ProductColor(models.Model):
    Product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=255)                  
    colors=models.CharField(choices=COLORS, max_length=20,default="no colors")


    def __str__(self):
        return self.colors

SIZES=(
      ("no sizes","no sizes"),
      ("uk=4","uk-4"),
      ("uk-5","uk-5"),
      ("uk-6","uk-6"),
      ("uk-7","uk-7"),
      ("uk-8","uk-8"),
      ("uk-9","uk-9"),
      ("uk-10","uk-10"),

)

class ProductSize(models.Model):
    Product = models.ForeignKey(Product, related_name='sizes',
                                on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    sizes = models.CharField(choices=SIZES, max_length=100, default='no sizes',null=True,blank=True)

    def __str__(self):
        return self.sizes



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    is_in_order = models.BooleanField(default=False)

    def __str__(self):
        return "Cart: " + str(self.id)
   
    def get_total_cost(self):

        return sum(item.get_cost() for item in self.cart.all())

class CartProduct(models.Model):
    cart = models.ForeignKey(
        Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE ,default="no_color")
    size=models.ForeignKey(ProductSize, on_delete=models.CASCADE, default="no_sizes")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)

    def get_cost(self):
        return self.price * self.quantity

     

class ShippingAddress(models.Model) :
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    name=models.CharField(max_length=55)
    city=models.CharField(max_length=55)
    pincode=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    destinationtype=models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    def __str__(self):
        return self.name


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
    address = models.ForeignKey(ShippingAddress,on_delete=models.CASCADE,null=False)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(
        default=False, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)
