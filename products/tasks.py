import logging
from sys import stderr

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import Template, Context
from mywebsite.celery import app

import logging


VERIFICATION_TEMPLATE = """
{{ message|safe }}
{{ message.sent_date }}

<a href="http://127.0.0.1:8000/user/{{uuid}}" class="close">Ok</a>
"""

logger = logging.getLogger(__name__)


@app.task
def send_verification_email():
    for user in User.objects.all():
        messages = user.messagewrapper_set.all()
        logger.debug(f'{user.username}\'s message queue: {messages}')
        if user.userprofile.verified or messages.count() == 0 or user.is_superuser:
            continue
        message = messages[0]
        template = Template(VERIFICATION_TEMPLATE)
        send_mail('You\'ve got a new message',
                  '',
                  'Luckstriker073@gmail.com',
                  [user.email],
                  fail_silently=False,
                  html_message=template.render(context=Context({'message': message,
                                                                'uuid': user.userprofile.verification_uuid})),
                  )

        message.delete()
        user.userprofile.verified = True
        user.save()

        logger.debug(f'Sent message to {user.username}')
        logger.debug(f'{user.username}\'s message queue: {messages}')



