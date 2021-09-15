from django.urls import path

from products.views import auth
from products.views import cart
from products.views import index


app_name = 'products'
urlpatterns = [
    path('', index.index, name="index"),
    path('register/', auth.register, name="register"),
    path('login/', auth.login_user, name="login"),
    path('logout/', auth.logout_user, name='logout'),
    path('<int:product_id>/cart', cart.user_cart_add, name="cart_add"),
    path('user/cart', cart.UserCartListView.as_view(), name="cart"),
    path('user/cart/<int:pk>/delete', cart.UserCartDeleteView.as_view(), name='cart_delete'),
    path('user/cart/<int:pk>/update', cart.UserCartUpdateView.as_view(), name='cart_update'),
    path('user/<uuid:uuid>/', auth.verify, name='verify')
]
