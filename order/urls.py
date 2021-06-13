from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addtocard/<int:id>', views.addtocart , name='addtocard'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('shopcart/', views.shopcart , name='shopcart' ),
    path('orderproduct/', views.orderproduct, name='orderproduct'),



]