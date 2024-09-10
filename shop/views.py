from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
from rest_framework import permissions

from .forms import OrderForm
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from .forms import ReceiptUploadForm


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
    product = get_object_or_404(Product, id=product_id)

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
            amount=amount,
            payment_method='bank',  # Set default payment method for redirection
            is_paid=False
        )

        # Redirect to payment choice page
        return redirect('payment_choice', order_id=order.id)

    return render(request, 'webapp.html', {'product': product})

@csrf_protect
def payment_choice_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = ReceiptUploadForm(request.POST, request.FILES)
        if form.is_valid():
            payment_method = form.cleaned_data.get('payment_method')
            receipt_file = form.cleaned_data.get('receipt_file')
            
            # Update the order with payment method and receipt
            order.payment_method = payment_method
            order.receipt_file = receipt_file
            order.save()

            # Redirect to success page
            return render(request, 'payment_success.html', {'order': order})

    else:
        form = ReceiptUploadForm()

    return render(request, 'payment_choice.html', {'form': form, 'order': order})