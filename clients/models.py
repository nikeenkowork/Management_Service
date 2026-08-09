from django.conf import settings
from django.db import models


class Recipient(models.Model):

    email = models.EmailField(
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
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения"
    )


    def __str__(self):
        return f"{self.full_name} ({self.email})"


    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["full_name"]

        constraints = [
            models.UniqueConstraint(
                fields=["owner", "email"],
                name="unique_recipient_email_for_user"
            )
        ]
