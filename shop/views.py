from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets

from .forms import OrderForm
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


def webapp_view(request):
    return render(request, 'webapp.html')