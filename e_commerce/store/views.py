from django.shortcuts import render,HttpResponse,redirect
import datetime
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
import json
from django.shortcuts import render, get_object_or_404

# Create your views here.

def Main(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items= []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
          cartItems = order['get_cart_items']
     context = {'cartItems':cartItems}
     return render(request, 'store/main.html', context)

def contact(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items= []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
          cartItems = order['get_cart_items']
     context = {'cartItems':cartItems}
     return render(request, 'store/contact.html', context)


def store(request):

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items= []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
          cartItems = order['get_cart_items']

     products = Product.objects.all()
     context = {'products':products,'cartItems':cartItems}
     return render(request, 'store/store.html', context)

def cart(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items= []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
          cartItems = order['get_cart_items']

     context = {'items':items, 'order':order,'cartItems':cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items= []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
          cartItems = order['get_cart_items']

     context = {'items':items, 'order':order,'cartItems':cartItems}
     return render(request, 'store/checkout.html', context)

def login(request):
     if request.method=='POST':
          username=request.POST.get('username')
          pass1=request.POST.get('pass')
          print(username,pass1)
          user=authenticate(request,username=username,password=pass1)
          if user is not None:
               auth_login(request,user)
               return redirect('Main')
          else:
               return redirect('login',)
               
     context = {}
     return render(request, 'store/login.html', context)

def signup(request):
     if request.method=='POST':
          uname=request.POST.get('username')
          email=request.POST.get('email')
          pass1=request.POST.get('password1')
          pass2=request.POST.get('password2')
          if pass1!=pass2:
               return HttpResponse("Your password and comfirmation password are different")
          my_user=User.objects.create_user(uname,email,pass1)
          my_user.save()

          customer = Customer(user=my_user)
          customer.save()
          return redirect('login')
          print(uname,email,pass1,pass2)

     context = {}
     return render(request, 'store/signup.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print('Action:', productId)
     print('productId:', productId)


     customer = request.user.customer
     product = Product.objects.get(id = productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order = order, product=product)
     
     if action == 'add':
          orderItem.quantity= (orderItem.quantity +1)
     elif action == 'remove':
          orderItem.quantity= (orderItem.quantity -1)
     
     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()
          

     return JsonResponse('Item was added', safe=False)

def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          total = float(data['form']['total'])
          order.transaction_id = transaction_id

          if total == order.get_cart_total:
               order.complete = True
          order.save()

          if order.shipping == True:
               ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
               )
     else:
          print('user is not logged in')
     return JsonResponse('Payment complete', safe=False)

