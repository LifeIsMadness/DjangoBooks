from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from products.forms import UserLoginForm, UserRegisterForm
from products.models.user import UserProfile

import logging
logger = logging.getLogger(__name__)


@login_required
def logout_user(request):
    logger.debug(f'{request.user.username} logged out.')
    logout(request)
    return redirect('products:login')


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            logger.debug(f'{new_user.username} registered.')
          #  cart = Cart.objects.create(user=new_user)
            return render(request, 'products/user_registered.html', {'new_user': new_user})
        else:
            messages.error(request, 'Something wrong. Please, try again')
    else:
        user_form = UserRegisterForm()
    return render(request, 'products/register.html', {'user_form': user_form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            temp = form.cleaned_data
            user = authenticate(username=temp['username'], password=temp['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.debug(f'{user.username} logged in.')
                    return redirect(request.POST['next']) if request.POST['next'] != '' else redirect('products:index')
                else:
                    return HttpResponse('Disabled account')
            else:
                # return HttpResponse('Invalid login or password')
                data = 'Invalid login or password'
                return render(request, 'products/login.html', {'form': form, 'data': data})
    else:
        form = UserLoginForm()
    return render(request, 'products/login.html', {'form': form})


def verify(request, uuid):
    user_profile = get_object_or_404(UserProfile, verification_uuid=uuid, verified=True)
    user = user_profile.user
    # user read the message, so now its possible to send new
    user.userprofile.verified = False
    user.save()
    logger.debug(f'{user.username} read the message')

    return redirect('products:index')
