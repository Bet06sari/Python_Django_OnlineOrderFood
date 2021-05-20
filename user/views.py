from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import Setting, UserProfile
from product.models import Catagory


def index(request):
    setting = Setting.objects.get(pk=1)
    catagory = Catagory.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'catagory': catagory,
               'setting': setting,
               'profile': profile }
    return render(request,'user_profile.html',context)
