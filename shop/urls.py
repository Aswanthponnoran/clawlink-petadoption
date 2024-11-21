from django.urls import path
from shop import views
app_name="shop"



urlpatterns = [
    path('', views.category, name='category'),
    path('index',views.index,name='nameindex'),
    path('base', views.base, name='base'),
    path('product/<int:prodtid>', views.product, name='product'),
    path('detail/<int:prodetilid>', views.productdetail, name='detail'),
    path('register', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('addcategories/', views.addcategories, name='addcategories'),
    path('addproducts/', views.addproducts, name='addproducts'),
    path('addstock/<int:adstkid>', views.addstock, name='addstock'),

]
