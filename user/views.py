from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from home.models import Setting, UserProfile
from product.models import Catagory
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    setting = Setting.objects.get(pk=1)
    catagory = Catagory.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'catagory': catagory,
               'setting': setting,
               'profile': profile }
    return render(request,'user_profile.html',context)




@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'your account has been updated')
            return redirect('/user')
    else:
        catagory = Catagory.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form =ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'catagory': catagory,
            'user_form': user_form,
            'profile_form': profile_form,

        }
        return render(request,'user_update.html',context)

@login_required(login_url='/login')  # Check login
def change_password(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        catagory = Catagory.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html',
                      {
                          'form': form,
                          'catagory': catagory,
                          'setting': setting,
        })