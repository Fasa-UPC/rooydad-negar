import json
from django.conf import settings
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from events_module.models import Event, Participant, UserDescount, Discount
from accounts_module.models import User
from django.utils import timezone
from django.db.models import F

# Create your views here.
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
CallbackURL = 'http://127.0.0.1:8000/payment/verify'


def request_payment(request):
    event = Participant.objects.filter(status=False, user=request.user).first()
    useable = UserDescount.objects.filter(user=request.user, status=False).first()
    if event:
        event_price = event.total
        capacity = Event.objects.get(id=event.event.id)

        if event_price == 0:
            event.status = True
            event.save()
            capacity.capacity = capacity.capacity - 1
            capacity.save()
            if useable:
                useable.status = True
                Discount.objects.filter(code=useable.code).update(count=F('count') - 1)
                useable.save()
            return redirect('payment:seccess')
    else:
        return redirect("events:events")
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": event_price,
        "Description": event.event.title,
        "Phone": request.user.phone_number,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                url = f"{ZP_API_STARTPAY}{response['Authority']}"
                return redirect(url)
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify_payment(request):
    authority = request.GET['Authority']
    event = Participant.objects.filter(status=False, user=request.user).first()
    if event:
        event_price = event.total
        capacity = Event.objects.get(id=event.event.id)
    else:
        return redirect("events:events")
    useable = UserDescount.objects.filter(user=request.user, status=False).first()

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": event_price,
        'Authority': authority,

    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    res = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    if res.status_code == 200:
        response = res.json()

        if response['Status'] == 100:
            event.status = True
            event.event.capacity = event.event.capacity - 1
            event.save()
            capacity.capacity = capacity.capacity - 1
            capacity.save()
            if useable:
                useable.status = True
                useable.save()
                Discount.objects.filter(code=useable.code).update(count=F('count') - 1)
            return redirect('payment:seccess')
        else:
            return redirect('payment:failur')
    else:
        return redirect('payment:failur')


def seccess_payment(request):
    return render(request, 'module/seccess.html')


def failur_payment(request):
    return render(request, 'module/failure.html')
