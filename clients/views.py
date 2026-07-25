from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Recipient
from .forms import RecipientForm



class RecipientListView(
    LoginRequiredMixin,
    ListView
):

    model = Recipient
    template_name = "clients/recipient_list.html"


    def get_queryset(self):
        return Recipient.objects.filter(
            owner=self.request.user
        )



class RecipientCreateView(
    LoginRequiredMixin,
    CreateView
):

    model = Recipient
    form_class = RecipientForm

    template_name = "clients/recipient_form.html"

    success_url = reverse_lazy(
        "clients:list"
    )


    def form_valid(self, form):

        form.instance.owner = (
            self.request.user
        )

        return super().form_valid(form)



class RecipientUpdateView(
    LoginRequiredMixin,
    UpdateView
):

    model = Recipient

    form_class = RecipientForm

    template_name = "clients/recipient_form.html"

    success_url = reverse_lazy(
        "clients:list"
    )


    def get_queryset(self):

        return Recipient.objects.filter(
            owner=self.request.user
        )



class RecipientDeleteView(
    LoginRequiredMixin,
    DeleteView
):

    model = Recipient

    template_name = "clients/recipient_confirm_delete.html"

    success_url = reverse_lazy(
        "clients:list"
    )


    def get_queryset(self):

        return Recipient.objects.filter(
            owner=self.request.user
        )
