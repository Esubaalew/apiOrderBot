from django import views
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, webapp_view, payment_choice_view

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('webapp/', webapp_view, name='webapp_view'),
     path('payment/<int:order_id>/', payment_choice_view, name='payment_choice'),
]
