from django.conf import settings
from django.db import models


class Recipient(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )

    full_name = models.CharField(
        max_length=150,
        verbose_name="Ф.И.О."
    )

    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipients",
        verbose_name="Владелец"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f"{self.full_name} ({self.email})"
