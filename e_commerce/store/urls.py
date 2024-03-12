from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('',views.Main, name='Main'),
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout_user, name="logout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    
]