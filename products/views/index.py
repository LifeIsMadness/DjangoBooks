from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from products.models.message import MessageWrapper
from products.models.product import Book

import logging
logger = logging.getLogger(__name__)


@login_required
def index(request):
    books = Book.objects.all()
    logger.debug(books)
    context = {'books': books}
    return render(request, 'products/index.html', context)

