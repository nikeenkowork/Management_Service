from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Mailing, MailingAttempt


def send_mailing(mailing: Mailing):
    now = timezone.now()

    if not (mailing.start_time <= now <= mailing.end_time):
        raise ValueError("Сейчас отправка запрещена по времени.")

    mailing.status = Mailing.STATUS_STARTED
    mailing.save(update_fields=["status"])

    success_count = 0

    for recipient in mailing.recipients.all():

        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient.email],
                fail_silently=False,
            )

            success_count += 1

            MailingAttempt.objects.create(
                mailing=mailing,
                status=MailingAttempt.STATUS_SUCCESS,
                server_response="Письмо успешно отправлено",
            )

        except Exception as error:

            MailingAttempt.objects.create(
                mailing=mailing,
                status=MailingAttempt.STATUS_FAILED,
                server_response=str(error),
            )

    mailing.status = Mailing.STATUS_FINISHED
    mailing.save(update_fields=["status"])

    return success_count
