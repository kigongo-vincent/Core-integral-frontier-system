from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django_resized import ResizedImageField


class User(AbstractUser):

    username = models.CharField(unique=True, null=True, blank=True, max_length=100)
    email = models.EmailField(unique=True, null=False)
    role = models.CharField(max_length=100, default="officer")
    OTP = models.CharField(max_length = 10, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    REQUIRED_FIELDS=['username'] # must be added to avoid complications when creating the super user
    USERNAME_FIELD = "email" #change the authentication field to take in email and password


class Product(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    photo = ResizedImageField(quality=60,upload_to="static/uploads/products",null=True, blank=True)
    photo2 = ResizedImageField(quality=60,upload_to="static/uploads/products",null=True, blank=True)
    price = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    type = models.TextField(null=True, blank=True)
    likers = models.ManyToManyField(User, related_name="likers", null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

class Order(models.Model):

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.JSONField()
    order_date = models.DateTimeField(auto_now_add=True, null=True)
    delivery_date = models.DateTimeField(null=True, blank = True)

    class Meta:
        ordering = ["-order_date"]
    

    def __str__(self):
        return str(self.order_date)


class Service(models.Model):

    title = models.CharField(max_length=100)
    about = models.TextField()

    def __str__(self):
        return self.title
