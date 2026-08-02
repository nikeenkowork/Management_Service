from django.conf import settings
from django.db import models
from django.utils import timezone


class Mailing(models.Model):

    STATUS_CREATED = "Создана"
    STATUS_STARTED = "Запущена"
    STATUS_FINISHED = "Завершена"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущена"),
        (STATUS_FINISHED, "Завершена"),
    ]

    start_time = models.DateTimeField(
        verbose_name="Дата и время начала отправки"
    )

    end_time = models.DateTimeField(
        verbose_name="Дата и время окончания отправки"
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name="Статус",
    )

    message = models.ForeignKey(
        "mail_messages.Message",
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="mailings",
    )

    recipients = models.ManyToManyField(
        "clients.Recipient",
        verbose_name="Получатели",
        related_name="mailings",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
    )


    def update_status(self):
        now = timezone.now()

        if now < self.start_time:
            new_status = self.STATUS_CREATED

        elif self.start_time <= now <= self.end_time:
            new_status = self.STATUS_STARTED

        else:
            new_status = self.STATUS_FINISHED

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=["status"])


    def __str__(self):
        return f"Рассылка №{self.pk}"


    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-start_time"]
