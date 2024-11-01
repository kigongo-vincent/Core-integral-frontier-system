from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from .serializers import *

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# customizing the information encoded in the access token by adding extra fields 
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod

    def get_token(cls, user):

        token = super().get_token(user)

        # Add custom claims to the token payload

        token['role'] = user.role

        token['email'] = user.email

        return token
    

# creating a custom serializer for information encoded in the tokens 

class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer


@api_view(["GET"])
def welcome(request):
    return Response([f"api/v1/token"])


@api_view(["POST"])
def signup(request):
    try:
        email = request.data["email"]
        password = make_password(request.data["password"])
        User.objects.create(
                email = email,
                password = password,
                role ="customer"
        )
        return Response(status=status.HTTP_201_CREATED)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def add_product(request):
    try:
        serialized = ProductSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
    except:
        print(serialized)
        return Response(status = status.HTTP_400_BAD_REQUEST)    

@api_view(['GET'])
def get_products(request, category):
    products = Product.objects.filter(type = category)
    serialized = ProductSerializer(products, many=True)
    return Response(serialized.data)


@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(id = pk)
        product.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_product(request, pk):
    try:
        product = Product.objects.get(id = pk)
        serialized = ProductSerializer(product, data=request.data, partial = True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_202_ACCEPTED)
        
        else:
            print(serialized.errors)
            return Response(status = status.HTTP_400_BAD_REQUEST)
        
    except:
        return Response(status=status.HTTP_418_IM_A_TEAPOT)    

@api_view(['GET'])
def all_products(request):
    products = Product.objects.all()
    serialized = ProductSerializer(products, many = True)
    return Response(serialized.data)

@api_view(['GET', 'POST'])
def customer_orders(request, pk):
    if request.method == "POST":
        serialized = OrderSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    orders = Order.objects.filter(customer = pk)
    serialized = OrderSerializer(orders, many = True)

    for item in serialized.data:
        products = item["products"]

        for product in products:
            found_product = Product.objects.get(id = product["id"])
            serialized_product = ProductSerializer(found_product)
            product["product"] = serialized_product.data


    return Response(serialized.data)    


@api_view(['POST'])
def change_password(request, pk):
    try:
        found_user =User.objects.get(id = pk)
        found_user.password = make_password(request.data["password"])
        found_user.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def search(request, query):
    products = Product.objects.filter(
        Q(name__icontains = query ) |
        Q(description__icontains = query ) |
        Q(type__icontains = query ) |
        Q(price__icontains = query ) |
        Q(brand__icontains = query ) |
        Q(photo__icontains = query )

    )  
    serialized = ProductSerializer(products, many =True)
    return Response(serialized.data)


@api_view(['GET', 'POST'])
def services(request):
    if request.method == "POST":
        serialized = ServiceSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    services = Service.objects.all()
    serialized = ServiceSerializer(services, many = True)
    return Response(serialized.data)    

@api_view(['GET'])
def orders(request):
    orders = Order.objects.all()
    serialized = OrderSerializer(orders, many = True)
    for item in serialized.data:
        products = item["products"]
        item["customer_email"] = UserSerializer(User.objects.get(id = item["customer"])).data["email"]
        for product in products:
            try:
                found_product = Product.objects.get(id = product["id"])
                serialized_product = ProductSerializer(found_product)
                product["product"] = serialized_product.data
            except:
                pass

    return Response(serialized.data)    


@api_view(['PATCH'])
def update_order(request, pk):
    try:
        found_order = Order.objects.get(id = pk)
        serialized = OrderSerializer(found_order, data = request.data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response(status=status.HTTP_418_IM_A_TEAPOT)            


@api_view(['GET'])
def customers(request):
    customers = User.objects.filter(role="customer")
    serialized = CustomerSerializer(customers, many = True)
    return Response(serialized.data)


@api_view(['PATCH'])
def update_customer(request, pk):
    try:
        customer = User.objects.get(id =pk, role="customer")
        serialized = UserSerializer(customer, data=request.data, partial = True)
        if serialized.is_valid():
            serialized.save()
            return Response(status=status.HTTP_202_ACCEPTED)   
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)    


@api_view(['GET'])
def statistics(request):

    customers = User.objects.filter(role="customer").count()
    services = Service.objects.all().count()
    orders = Order.objects.all().count()
    products = Product.objects.all()

    categories = 0

    # for product in products:
    #     if not product['category'] in categories:
    #         categories += 1

    stats = {
        "customers": customers,
        "services": services,
        "orders": orders,
        "products": products.count()
    }

    return Response(stats)



