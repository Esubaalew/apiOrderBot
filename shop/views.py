from rest_framework import viewsets
from rest_framework import permissions
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


from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Order
from .forms import ReceiptUploadForm
import logging

logger = logging.getLogger(__name__)


@csrf_protect
def webapp_view(request):
    logger.info(f"Request Method: {request.method}")
    logger.info(f"Query Parameters: {request.GET}")

    start_param = request.GET.get('tgWebAppStartParam', '')

    logger.info(f"Start Parameter: {start_param}")

    if start_param.startswith('product-'):
        try:
            product_id = start_param.split('-')[1]
            logger.info(f"Product ID extracted: {product_id}")

            product = get_object_or_404(Product, id=product_id)
            logger.info(f"Product found: {product.name} (ID: {product.id})")

        except (IndexError, ValueError):
            logger.error("Error extracting product ID from start_param")
            return render(request, '404.html', {'error': 'Invalid product ID'})

    else:
        logger.error("Invalid start_param, does not start with 'product-'")
        return render(request, '404.html', {'error': 'Product not found'})

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        comment = request.POST.get('comment', '')
        quantity = int(request.POST.get('quantity', 1))

        total_price = product.price * quantity

        order = Order.objects.create(
            product=product,
            full_name=full_name,
            address=address,
            phone_number=phone_number,
            comment=comment,
            quantity=quantity,
            total_price=total_price,
            payment_method='bank',
            is_paid=False
        )

        return redirect('payment_choice', order_id=order.id)

    logger.info(f"Rendering product page for product: {product.name}")
    return render(request, 'webapp.html', {'product': product})


@csrf_protect
def payment_choice_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = ReceiptUploadForm(request.POST, request.FILES)
        if form.is_valid():
            payment_method = form.cleaned_data.get('payment_method')
            receipt_file = form.cleaned_data.get('receipt_file')

            order.payment_method = payment_method
            order.receipt_file = receipt_file
            order.save()

            return render(request, 'payment_success.html', {'order': order})

    else:
        form = ReceiptUploadForm()

    return render(request, 'payment_choice.html', {'form': form, 'order': order})
