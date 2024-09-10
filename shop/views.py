from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework import permissions

from .forms import OrderForm
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@method_decorator(csrf_exempt, name='dispatch')
class OrderViewSet(viewsets.ModelViewSet):
    # define permission
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@csrf_protect
def webapp_view(request):
    product_id = request.GET.get('product_id')
    print(product_id)
    product = get_object_or_404(Product, id=product_id)
    print(product)

    if request.method == 'POST':
        # Retrieve form data
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        comment = request.POST.get('comment', '')  # Optional
        amount = request.POST.get('amount')

        # Create the order
        order = Order.objects.create(
            product=product,
            full_name=full_name,
            address=address,
            phone_number=phone_number,
            comment=comment,
            amount=amount
        )

        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Order created successfully!'})

    return render(request, 'webapp.html', {'product': product})
