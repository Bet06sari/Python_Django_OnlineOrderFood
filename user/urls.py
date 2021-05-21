from django.urls import path

from . import views

urlpatterns = [
    # ex:/home/
    path('', views.index, name='index'),
    path('update/', views.user_update, name="user_update"),
    path('password/', views.change_password, name="change_password"),

    #path('addcomment/<int:id>', views.addcomment, name='addcomment')

    # ex:/home/5/
    #path('<int:question_id>/', views.detail, name='detail'),

]