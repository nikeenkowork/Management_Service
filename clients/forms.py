from django import forms

from .models import Recipient


class RecipientForm(forms.ModelForm):

    class Meta:
        model = Recipient

        fields = [
            "email",
            "full_name",
            "comment",
        ]

        widgets = {"comment": forms.Textarea(attrs={"rows": 4})}
