from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Mailing
from .forms import MailingForm


class MailingListView(
    LoginRequiredMixin,
    ListView
):
    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        return Mailing.objects.filter(
            owner=self.request.user
        )


class MailingDetailView(
    LoginRequiredMixin,
    DetailView
):
    model = Mailing
    template_name = "mailing/mailing_detail.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # автоматическое обновление статуса
        obj.update_status()

        return obj


class MailingCreateView(
    LoginRequiredMixin,
    CreateView
):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy(
        "mailing:list"
    )

    def form_valid(self, form):
        form.instance.owner = self.request.user

        response = super().form_valid(form)

        self.object.update_status()

        return response


class MailingUpdateView(
    LoginRequiredMixin,
    UpdateView
):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy(
        "mailing:list"
    )

    def get_queryset(self):
        return Mailing.objects.filter(
            owner=self.request.user
        )

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object.update_status()

        return response


class MailingDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy(
        "mailing:list"
    )

    def get_queryset(self):
        return Mailing.objects.filter(
            owner=self.request.user
        )
    