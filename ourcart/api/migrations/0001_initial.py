# Generated by Django 4.0.5 on 2022-07-01 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, default=None, max_length=60, null=True, unique=True, verbose_name='email')),
                ('city', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('username', models.CharField(blank=True, max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_super_teacher', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'authusers',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='banners/')),
            ],
            options={
                'db_table': 'Banners',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('complit', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('is_in_order', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Cart',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='categories/')),
            ],
            options={
                'db_table': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='products/')),
                ('marked_price', models.PositiveIntegerField()),
                ('selling_price', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('warranty', models.CharField(blank=True, max_length=300, null=True)),
                ('return_policy', models.CharField(blank=True, max_length=300, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
            ],
            options={
                'db_table': 'Products',
            },
        ),
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=150)),
                ('fileDesc', models.CharField(max_length=150)),
                ('myfile', models.FileField(upload_to='uploads/')),
                ('date', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'Uploads',
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('city', models.CharField(max_length=55)),
                ('pincode', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('destinationtype', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Shipping_Address',
            },
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sizes', models.CharField(choices=[('no sizes', 'no sizes'), ('uk=4', 'uk-4'), ('uk-5', 'uk-5'), ('uk-6', 'uk-6'), ('uk-7', 'uk-7'), ('uk-8', 'uk-8'), ('uk-9', 'uk-9'), ('uk-10', 'uk-10')], default='no sizes', max_length=100)),
                ('Product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='api.product')),
            ],
            options={
                'db_table': 'Products_Sizes',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('images', models.ImageField(upload_to='Productimages/')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.product')),
            ],
            options={
                'db_table': 'Products_Images',
            },
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('colors', models.CharField(choices=[('no colors', 'no colors'), ('Red', 'Red'), ('Green', 'Green'), ('Yellow', 'Yellow'), ('Pink', 'Pink'), ('Brown', 'Brown'), ('Black', 'Black'), ('White', 'White')], default='no colors', max_length=20)),
                ('Product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='api.product')),
            ],
            options={
                'db_table': 'Products_Colors',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_by', models.CharField(max_length=200)),
                ('subtotal', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('order_status', models.CharField(choices=[('Order Received', 'Order Received'), ('Order Processing', 'Order Processing'), ('On the way', 'On the way'), ('Order Completed', 'Order Completed'), ('Order Canceled', 'Order Canceled')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(choices=[('Cash On Delivery', 'Cash On Delivery'), ('Khalti', 'Khalti'), ('Esewa', 'Esewa')], default='Cash On Delivery', max_length=20)),
                ('payment_completed', models.BooleanField(blank=True, default=False, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.shippingaddress')),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.cart')),
            ],
            options={
                'db_table': 'Product_Orders',
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('delivery_charge', models.PositiveBigIntegerField(default=100)),
                ('quantity', models.PositiveIntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cart')),
                ('color', models.ForeignKey(default='no_color', on_delete=django.db.models.deletion.CASCADE, to='api.productcolor')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
                ('size', models.ForeignKey(default='no_sizes', on_delete=django.db.models.deletion.CASCADE, to='api.productsize')),
            ],
            options={
                'db_table': 'Cart_Items',
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='admins/')),
                ('mobile', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
