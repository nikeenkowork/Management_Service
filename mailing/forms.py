from django import forms
from django.utils import timezone

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
                attrs={
                    "type": "datetime-local"
                }
            ),

            "end_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            ),

            "recipients": forms.SelectMultiple(
                attrs={
                    "class": "form-control"
                }
            ),
        }


    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get(
            "start_time"
        )

        end_time = cleaned_data.get(
            "end_time"
        )


        if start_time:

            if start_time < timezone.now():
                raise forms.ValidationError(
                    "Дата начала рассылки не может быть в прошлом."
                )


        if start_time and end_time:

            if start_time >= end_time:
                raise forms.ValidationError(
                    "Дата начала должна быть раньше даты окончания."
                )


        return cleaned_data
