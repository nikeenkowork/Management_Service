from django import forms
from django.utils import timezone

from clients.models import Recipient
from mail_messages.models import Message

from .models import Mailing


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing

        fields = (
            "start_time",
            "end_time",
            "message",
            "recipients",
        )

        widgets = {
            "start_time": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                },
            ),
            "end_time": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                },
            ),
            "recipients": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                },
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:

            # только свои сообщения
            self.fields["message"].queryset = Message.objects.filter(owner=user)

            # только свои получатели
            self.fields["recipients"].queryset = Recipient.objects.filter(owner=user)

    def clean(self):

        cleaned_data = super().clean()

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and start_time < timezone.now():

            raise forms.ValidationError("Дата начала рассылки не может быть в прошлом.")

        if start_time and end_time and start_time >= end_time:

            raise forms.ValidationError(
                "Дата начала должна быть раньше даты окончания."
            )

        return cleaned_data
