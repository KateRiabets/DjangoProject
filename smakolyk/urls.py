from . import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contacts/', views.contacts, name='contacts'),
    path('', views.home, name='home'),
    path('store/', views.store_view, name='store'),
    path('welcome/', views.welcome, name='welcome'),
    path('why/', views.why, name='why'),
    path('product/<str:name>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('get_cart_info/', views.get_cart_info, name='get_cart_info'),
    path('update_cart/', views.update_cart, name='update_cart'),


]
