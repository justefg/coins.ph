from django.shortcuts import render
from django.http import JsonResponse
from .models import Account, Payment, TransactionStatus
from django.core import serializers

def create_user(request, name, email):
    u = Account.objects.create(name=name, email=email)
    return JsonResponse({'status': 'created'})

def get_user(req, name):
    u = Account.objects.get(name=name)
    incoming, outgoing = get_payments(name)
    print('>>>', serializers.serialize('json', incoming))
    print('>>>', serializers.serialize('json', outgoing))
    return JsonResponse({'name': name, 'email': u.email,
                         #'incoming': serializers.serialize('json', incoming),
                         #'outgoing': serializers.serialize('json', outgoing),
                         'balance': get_balance(incoming, outgoing)})


def get_payments(name):
    outgoing = Payment.objects.filter(source=name, status=TransactionStatus.COMPLETED)
    incoming = Payment.objects.filter(destination=name, status=TransactionStatus.COMPLETED)
    return incoming, outgoing


def count_amount(payments):
    result = 0
    for p in payments:
        result += p.amount
    return result


def get_balance(incoming, outgoing):
    incoming_amount = count_amount(incoming)
    outgoing_amount = count_amount(outgoing)
    return incoming_amount - outgoing_amount


def transfer(req, src, dst, amount):
    amount /= 1_00
    p = Payment.objects.create(source=Account.objects.get(name=src),
                               destination=Account.objects.get(name=dst),
                               amount=amount)
    return JsonResponse({'tx_id': p.id, 'status': p.status.value})

