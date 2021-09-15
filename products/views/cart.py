from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DeleteView, ListView

from products.models.cart import CartElement
from products.models.product import Book

import logging
logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class UserCartUpdateView(UpdateView):
    model = CartElement
    template_name = 'products/update.html'
    success_url = reverse_lazy('products:cart')
    fields = ('count',)


@method_decorator(login_required, name='dispatch')
class UserCartDeleteView(DeleteView):
    model = CartElement
    template_name = 'products/delete.html'
    success_url = reverse_lazy('products:cart')

    # Overriding dispatch to avoid 404,
    # if user clicks prev page button
    def dispatch(self, request, *args, **kwargs):
        try:
            cart_element = CartElement.objects.get(id=kwargs['pk'])
            if request.method == 'GET':
                return super().dispatch(request, args, kwargs)
            else:
                cart_element.delete()
                return redirect(self.success_url)
        except CartElement.DoesNotExist:
            return redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class UserCartListView(ListView):
    model = CartElement

    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        products = user.cart.cartelement_set
        return render(request, 'products/cart.html', {'user': user, 'cart_elements': products})


@login_required
def user_cart_add(request, product_id):
    user = User.objects.get(id=request.user.id)
    try:
        product = Book.objects.get(id=product_id)
    except Book.DoesNotExist:
        logging.error('Book.DoesNotExist')
        raise Http404('No such book in the query')
    try:
        user.cart.cartelement_set.get(product=product)
    except CartElement.DoesNotExist:
        cart_element = CartElement.objects.create(product=product, cart=user.cart)
    products = user.cart.cartelement_set
    logger.debug(f'{user.username}\'s cart: {products.all()}')
    return redirect('products:cart')
