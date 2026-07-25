from django.conf import settings
from django.db import models


class Message(models.Model):
    subject = models.CharField(
        max_length=255,
        verbose_name="Тема сообщения"
    )

    body = models.TextField(
        verbose_name="Текст сообщения"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец"
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]

    def __str__(self):
        return self.subject
