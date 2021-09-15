import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

#from products.tasks import send_verification_email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_unread_message = models.BooleanField(name='verified', default=False)
    verification_uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


# @receiver(post_save, sender=User)
# def user_post_save(sender, instance, signal, *args, **kwargs):
#     if not instance.userprofile.verified:
#         offset = reverse("products:verify", kwargs={"uuid": str(instance.userprofile.verification_uuid)})
#         # send_mail('Verify your account',
#         #           'Follow this link to verify your account: '
#         #           f'http://localhost:8000{offset}',
#         #           'Luckstriker073@gmail.com',
#         #           [instance.email],
#         #           fail_silently=False,
#         #           )
#         #send_verification_email.delay()
