
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from django.db import transaction



class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام دسته')

    class Meta:
        verbose_name = ' دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='دسته بندی')
    name = models.CharField(max_length=200,verbose_name='نام محصول')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=10, decimal_places=0,verbose_name='قیمت')
    stock = models.PositiveIntegerField(verbose_name='موجودی',default=0,validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/', null=True, blank=True,verbose_name='تصویر')
    available = models.BooleanField(default=True,verbose_name='موجود است')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='ایجاد شده')


    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'




    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در حال بررسی'),
        ('processing', 'در حال پردازش'),
        ('completed', 'تکمیل شد'),
        ('cancelled', 'لغو شد'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='ایجاد شده')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',verbose_name='وضعیت سفارش')
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0,verbose_name='قیمت کل')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE,verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='محصول')
    quantity = models.PositiveIntegerField(verbose_name='مقدار')
    price = models.DecimalField(max_digits=10, decimal_places=0,verbose_name='هزینه')

    class Meta:
        verbose_name = 'مورد سفارش'
        verbose_name_plural = 'موارد سفارش'
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
   



phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="شماره تماس باید به این فرمت باشد: '+999999999'"
)

class CustomUser(AbstractUser):
    phone_number = phone_number = models.CharField(
        max_length=15,
        validators=[phone_validator],
        verbose_name='شماره تماس'
    )
    address = models.TextField(verbose_name='آدرس')
    
    def __str__(self):
        return self.username
    


def save(self, *args, **kwargs):
    if not self.pk:
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=self.product.pk)
            if self.quantity > product.stock:
                raise ValueError("موجودی کافی نیست")
            product.stock -= self.quantity
            product.save()
            super().save(*args, **kwargs)
    else:
        super().save(*args, **kwargs)





