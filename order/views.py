from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import Setting, UserProfile
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Catagory, Product


def index(reuqest):
    return HttpResponse("Order app")

@login_required(login_url='/login')
def addtocart(request,id):
    url=request.META.get('HTTP_REFERER')
    current_user=request.user

    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control = 1
    else:
        control = 0

    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():

            if control == 1:
                data = ShopCart.objects.get(product_id = id)
                data.quantity += form.cleaned_data['quantity']
                data.save()

            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = 1
                data.save()
                request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Ürün başarı ile sepete eklenmiştir.Teşekkür Ederiz")
        return HttpResponseRedirect(url)

    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            current_user = request.user
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Ürün başarı ile sepete eklenmiştir.Teşekkür Ederiz")
        return HttpResponseRedirect(url)

    messages.warning(request, "Ürün Sepete eklemede hata oluştu!. Lütfen kontrol ediniz ")
    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def shopcart(request):
    catagory=Catagory.objects.all()
    current_user=request.user
    setting = Setting.objects.get(pk=1)
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    total=0

    for rs in shopcart:
        total += rs.product.price * rs.quantity

    context={'catagory':catagory,
             'shopcart':shopcart,
             'total': total,
             'setting':setting,
             }
    return render(request,'Shopcart_products.html',context)

@login_required(login_url='/login')
def deletefromcart(request,id):
    catagory = Catagory.objects.all()
    setting = Setting.objects.get(pk=1)
    ShopCart.objects.filter(id=id).delete()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Ürün sepetten silinmiştir")
    context = {'category': catagory,
               'setting': setting,
              }

    return HttpResponseRedirect("/order/shopcart", context)

@login_required(login_url='/login')
def orderproduct(request):
    catagory = Catagory.objects.all()
    current_user=request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    if request.method =='POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.total = total
            data.user_id = current_user.id

            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id   = data.id
                detail.product_id = rs.product_id
                detail.user_id    = current_user.id
                detail.quantity   = rs.quantity
                detail.quantity   = rs.product.price
                detail.amount = rs.amount
                detail.save()
                # ***************< Reduce >***************#

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
                #***************<^^^^^^^^^^>***************#

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, "Siparisiniz tamamlandı!")
            return render(request, 'Order_Complated.html',
                          {'ordercode': ordercode,
                           'catagory': catagory
                           })
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'catagory': catagory,
               'total': total,
               'profile': profile,
               'form': form,
               }

    return render(request, 'Order_Form.html', context)