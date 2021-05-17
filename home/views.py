from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import json

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactFormu, ContactFormMessage
from product.models import Product, Catagory, Images, Comment


def index(request ):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[16:35]
    catagory = Catagory.objects.all()
    dayproducts=Product.objects.all()[30:31]
    lastproducts=Product.objects.all()[15:16]

    context = {'setting': setting,
               'catagory': catagory,
               'page':'home',
               'sliderdata':sliderdata,
               'dayproducts':dayproducts,
               'lastproducts':lastproducts
               }
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

def product_detail(request,id,slug):
    catagory = Catagory.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'product': product,
               'catagory': catagory,
               'images': images,
               'comments': comments,
               }
    return render(request,'product_detail.html',context)

def product_search(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':  # Check form post
        form = SearchForm(request.POST)  # Get form data
        if form.is_valid():
            catagory = Catagory.objects.all()
            query = form.cleaned_data['query']  # Get form data
            catid = form.cleaned_data['catid']

            if catid == 0:
                products = Product.objects.filter(title__icontains=query)  # Select * from Book where title like %query%
            else:
                products = Product.objects.filter(title__icontains=query, catagory_id=catid)

            context = {'products': products,
                       'catagory': catagory,
                       'setting': setting
                       }
            return render(request, 'product_search.html', context)

    return HttpResponseRedirect('/')

def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

