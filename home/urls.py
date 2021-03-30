from django.urls import path, include

from . import views, admin

urlpatterns = [
    # ex:/home/
    path('', views.index, name='index'),
    # ex:/home/5/
    #path('<int:question_id>/', views.detail, name='detail'),

]