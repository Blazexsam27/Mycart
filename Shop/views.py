from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate, Ads
from django.conf import settings
from math import ceil
from .paytm import generate_checksum, verify_checksum
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    ads = Ads.objects.all()
    allProducts = []
    catProducts = Product.objects.values('category', 'id')
    # fetching all types of categories.
    categories = {item['category'] for item in catProducts}

    for category in categories:
        products = Product.objects.filter(category=category)
        n = len(products)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProducts.append([products, range(1, nSlides), nSlides])
    params = {"allProducts": allProducts, 'ads': ads}

    return render(request, 'shop/index.html', params)


def searchItem(query, item):
    if query.lower() in item.product_desc.lower() or query.lower() in item.product_name.lower() or query.lower() in item.category.lower():
        return True
    return False


def search(request):
    query = request.GET.get('search', '')
    allProducts = []
    catProducts = Product.objects.values('category', 'id')
    # fetching all types of categories.
    categories = {item['category'] for item in catProducts}

    for category in categories:
        tempProducts = Product.objects.filter(category=category)
        products = [item for item in tempProducts if searchItem(query, item)]
        n = len(products)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(products) != 0:
            allProducts.append([products, range(1, nSlides), nSlides])
    params = {"allProducts": allProducts, "msg": "", "msglength": 0}
    if len(allProducts) == 0 or len(query) <= 2:
        params = {"allProducts": allProducts,
                  "msg": "No Match Found For Your Search!", "msglength": 1}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        contactNo = request.POST.get('contactNo', '')
        query = request.POST.get('query', '')
        contact = Contact(name=name, email=email,
                          contactNo=contactNo, desc=query)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method == 'POST':
        orderId = request.POST.get('orderId', "")
        email = request.POST.get('email', "")
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(
                        {"status": "success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "failed"}')
        except Exception as e:
            return HttpResponse('{"status": "error"}')
    return render(request, 'shop/tracker.html')


def productView(request, id):
    product = Product.objects.filter(id=id)
    category = product[0].category
    recommendations = Product.objects.filter(category=category).exclude(id=id)
    return render(request, 'shop/productView.html', {"product": product[0], "recommendations": recommendations})


def checkout(request):
    thank = False
    id = ""
    if request.method == 'GET':
        return render(request, 'shop/checkout.html', {'thanks': thank, 'id': id})
    if request.method == 'POST':
        items_json = request.POST.get('itemsJSON', "")
        name = request.POST.get('inputname', "")
        amount = request.POST.get('amount', "")
        email = request.POST.get('inputEmail', "")
        address = request.POST.get(
            'inputAddress', "") + " " + request.POST.get('inputAddress2', "")
        city = request.POST.get('inputCity', "")
        state = request.POST.get('inputState', "")
        zip_code = request.POST.get('inputZip', "")
        phone = request.POST.get('inputphone', "")
        order = Order(name=name, email=email, address=address,
                      city=city, state=state, zip_code=zip_code, phone=phone, items_json=items_json, amount=amount)
        thank = True
        order.save()
        update_order = OrderUpdate(
            order_id=order.order_id, update_desc="This order is placed")
        update_order.save()
        id = order.order_id
        # request paytm to transfer amount to your account after the payment.
        merchant_key = settings.PAYTM_SECRET_KEY
        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(id)),
            ('CUST_ID', str(order.email)),
            ('TXN_AMOUNT', str(order.amount))
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            # ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/')
        )
        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)
        paytm_params['CHECKSUMHASH'] = checksum
    return render(request, 'shop/redirect.html', context=paytm_params)


@csrf_exempt
def handlerequest(request):
    # paytm will send post request here
    # since it sends a post request we need to bypass our csrf check
    pass
