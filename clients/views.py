from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import RecipientForm
from .models import Recipient


class RecipientListView(
    LoginRequiredMixin,
    ListView,
):
    model = Recipient
    template_name = "clients/recipient_list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientCreateView(
    LoginRequiredMixin,
    CreateView,
):
    model = Recipient
    form_class = RecipientForm
    template_name = "clients/recipient_form.html"
    success_url = reverse_lazy("clients:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user

        response = super().form_valid(form)

        cache.delete(f"home_stats_user_{self.request.user.id}")

        return response


class RecipientUpdateView(
    LoginRequiredMixin,
    UpdateView,
):
    model = Recipient
    form_class = RecipientForm
    template_name = "clients/recipient_form.html"
    success_url = reverse_lazy("clients:list")

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)

        cache.delete(f"home_stats_user_{self.request.user.id}")

        return response


class RecipientDeleteView(
    LoginRequiredMixin,
    DeleteView,
):
    model = Recipient
    template_name = "clients/recipient_confirm_delete.html"
    success_url = reverse_lazy("clients:list")

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)

        cache.delete(f"home_stats_user_{self.request.user.id}")

        return response
