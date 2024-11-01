from rest_framework.serializers import ModelSerializer, CharField, FileField
from .models import *

class UserSerializer(ModelSerializer):

    class Meta:

        model = User

        fields= "__all__"

class CustomerSerializer(ModelSerializer):

    class Meta:

        model = User

        fields= ["email", "date_joined", "is_active", "id"]

class ProductSerializer(ModelSerializer):

    class Meta:

        model = Product

        fields= "__all__"

class OrderSerializer(ModelSerializer):

    class Meta:

        model = Order

        fields= "__all__"


class ServiceSerializer(ModelSerializer):

    class Meta:

        model = Service

        fields= "__all__"
