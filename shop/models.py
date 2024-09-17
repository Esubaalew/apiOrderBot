from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    PAYMENT_METHODS = [
        ('bank', 'Bank'),
        ('chapa', 'Chapa'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    comment = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)  # Default quantity is 1
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field for total price
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='bank')
    receipt_file = models.FileField(upload_to='receipts/', blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"



