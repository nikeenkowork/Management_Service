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

    start_time = models.DateTimeField(verbose_name="Дата и время начала отправки")

    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name="Статус",
    )

    message = models.ForeignKey(
        "mail_messages.Message",
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Сообщение",
    )

    recipients = models.ManyToManyField(
        "clients.Recipient",
        related_name="mailings",
        verbose_name="Получатели",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Владелец",
    )

    def update_status(self):
        now = timezone.now()

        if now < self.start_time:
            self.status = self.STATUS_CREATED
        elif self.start_time <= now <= self.end_time:
            self.status = self.STATUS_STARTED
        else:
            self.status = self.STATUS_FINISHED

        self.save(update_fields=["status"])

    def __str__(self):
        return f"Рассылка №{self.pk}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-start_time"]


class MailingAttempt(models.Model):

    STATUS_SUCCESS = "Успешно"
    STATUS_FAILED = "Не успешно"

    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Успешно"),
        (STATUS_FAILED, "Не успешно"),
    ]

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка",
    )

    attempt_time = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата и время попытки",
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        verbose_name="Статус",
    )

    server_response = models.TextField(
        blank=True,
        verbose_name="Ответ почтового сервера",
    )

    def __str__(self):
        return f"{self.mailing} - {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["-attempt_time"]
