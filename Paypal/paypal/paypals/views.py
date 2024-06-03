from django.shortcuts import render

import paypalrestsdk
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def create_payment(request):
    # Access form data from POST request
    intent = request.POST.get('intent')
    name = request.POST.get('name')
    price = request.POST.get('price')
    quantity = request.POST.get('quantity')
    total = request.POST.get('total')
    short_description = request.POST.get('short_description')

    payment = paypalrestsdk.Payment({
        "intent": intent,
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://example.com/payment/execute/",
            "cancel_url": "http://example.com/payment/cancel/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": name,
                    "sku": "item",
                    "price": price,
                    "currency": "USD",
                    "quantity": quantity
                }]
            },
            "amount": {
                "total": total,
                "currency": "USD"
            },
            "description": short_description
        }]
    })

    if payment.create():
        approval_url = [link.href for link in payment.links if link.rel == 'approval_url'][0]
        return JsonResponse({'approval_url': approval_url})
    else:
        return JsonResponse({'error': payment.error})
    
def index(request):
    return render(request,"index.html")
