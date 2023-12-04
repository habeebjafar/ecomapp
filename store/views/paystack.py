from django.shortcuts import render

def paystack_payment(request):
    return render(request, 'paystack.html')