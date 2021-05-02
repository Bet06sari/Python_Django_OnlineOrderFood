from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage
from product.models import Product, Catagory


def index(request ):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[3:23]
    catagory = Catagory.objects.all()

    context = {'setting': setting,
               'catagory': catagory,
               'page':'home',
               'sliderdata':sliderdata}
    return render(request, 'index.html', context)

def hakkimizda(request ):
    setting = Setting.objects.get(pk=1)
    catagory = Catagory.objects.all()
    context = {'setting' : setting, 'catagory': catagory}
    return render(request, 'hakkimizda.html', context)

def referanslar(request ):
    setting = Setting.objects.get(pk=1)
    catagory = Catagory.objects.all()
    context = {'setting' : setting, 'catagory': catagory}
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):

    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip= request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"mesajınız başarı ile gönderilmiştir. Teşekkür ederiz.")
            return HttpResponseRedirect ('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    catagory = Catagory.objects.all()
    context = {'setting': setting, 'form':form , 'catagory': catagory}
    return render(request, 'iletisim.html', context)

def catagory_products(request,id,slug):
    catagory = Catagory.objects.all()
    catagorydata = Catagory.objects.get(pk=id)
    products = Product.objects.filter(catagory_id=id)
    context = {'products': products,
               'catagory': catagory,
               'catagorydata': catagorydata,
               }
    return render(request,'products.html', context)
