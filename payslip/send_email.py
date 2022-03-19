from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import get_connection
from django.conf import settings

import traceback
import logging
import sys


# db_logger = logging.getLogger('db')


def send_email(email_list, subject, template_name, context, reply_to=None):

    msg_html = render_to_string(template_name, context)

    try:
        connection = get_connection()
        email = EmailMultiAlternatives(
            subject = subject,
            body = msg_html,
            from_email = settings.DEFAULT_FROM_EMAIL,
            to = email_list,
            connection=connection,
            reply_to = reply_to
        )

        email.attach_alternative(msg_html, 'text/html')
        email.send()
        return ('success')

    except Exception as e:
        # db_logger.exception(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])