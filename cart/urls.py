from django.urls import path
from cart import views
app_name="cart"



urlpatterns = [
    path('add<int:addcarts>/', views.addtocarts, name="addtocarts"),
    path('cartview/',views.cart_view,name='cartview'),
    path('cart_remove/<int:m>',views.cart_remove,name='cart_remove'),
    path('cart_delete/<int:m>', views.cart_delete, name='cart_delete'),
    path('orderform/', views.orderform, name='orderform'),
    path('orderview/', views.orderview, name='orderview'),
    path('payment-status<str:p>/', views.payment_status, name='payment_status'),

]
