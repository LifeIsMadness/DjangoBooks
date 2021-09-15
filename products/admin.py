from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .forms import MessageForm
from .models.message import MessageWrapper
from .models.product import Book
from .models.user import UserProfile
from .tasks import send_verification_email

import logging
logger = logging.getLogger(__name__)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'stock')
    fields = ('name', 'author', 'cost', 'stock', 'page_count', 'image')


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'
    fk_name = 'user'


class ExtendedUserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'is_verified', 'admin_actions')
    list_select_related = ('userprofile',)

    def is_verified(self, instance):
        return instance.userprofile.verified

    is_verified.short_description = 'verified'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(r'^(?P<user_id>.+)/message/$',
                self.admin_site.admin_view(self.notify_user),
                name='user_message')
        ]
        return custom_urls + urls

    def admin_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Notify</a>&nbsp;',
            reverse('admin:user_message', args=[obj.pk])
        )

    admin_actions.short_description = 'Actions'
    admin_actions.allow_tags = True

    def notify_user(self, request, user_id, *args, **kwargs):
        return self.notify_action(
            request=request,
            user_id=user_id,
            action_form=MessageForm,
        )

    def notify_action(self, request, user_id, action_form):
        user = self.get_object(request, user_id)

        MessageWrapper.objects.create(text='Test message', sent_date=timezone.now(), addressee=user)
        logger.debug(f'New message was added to {user.username}\'s queue')
        # send_verification_email()
        return HttpResponseRedirect('/admin/auth/user/')


admin.site.register(Book, ProductAdmin)
admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
