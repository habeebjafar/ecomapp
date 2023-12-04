from django.contrib import admin
from django.urls import path
from .views.home import Index , store, payment
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.orders import OrderView 
from .middlewares.auth import  auth_middleware
from .views.paystack import paystack_payment
from .views.register import  register, activate, forgot_account, forgot_account_link, recover_account


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),
    path('payment', payment , name='payment'),

    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('paystack/', paystack_payment, name='paystack'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    path('forgot_account', forgot_account, name='forgot_account'),
    path('forgot_account_link/<uidb64>/<token>/', forgot_account_link, name='forgot_account_link'),
    path('recover_account/<userId>/<token>/', recover_account, name='recover_account'),

]