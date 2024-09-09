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
    product_id = request.GET.get('product_id')  # Get product_id from query parameters
    product = get_object_or_404(Product, id=product_id)  # Fetch the specific product

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save the order with the product information
            order = form.save(commit=False)
            order.product = product  # Associate the order with the product
            order.save()
            return render(request, 'order_success.html')  # Success page
    else:
        form = OrderForm()

    return render(request, 'webapp_form.html', {'form': form, 'product': product})