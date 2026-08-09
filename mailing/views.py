from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from clients.models import Recipient
from .forms import MailingForm
from .models import Mailing
from .services import send_mailing


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        return Mailing.objects.filter(
            owner=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()

        context["total_mailings"] = Mailing.objects.filter(
            owner=self.request.user
        ).count()

        context["active_mailings"] = Mailing.objects.filter(
            owner=self.request.user,
            start_time__lte=now,
            end_time__gte=now,
            status=Mailing.STATUS_STARTED,
        ).count()

        context["total_recipients"] = Recipient.objects.filter(
            owner=self.request.user
        ).count()

        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"
    context_object_name = "mailing"

    def get_queryset(self):
        return Mailing.objects.filter(
            owner=self.request.user
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.object.update_status()
        return response


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        return Mailing.objects.filter(
            owner=self.request.user
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.update_status()
        return response


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:list")

    def get_queryset(self):
        return Mailing.objects.filter(
            owner=self.request.user
        )


def start_mailing(request, pk):
    mailing = get_object_or_404(
        Mailing,
        pk=pk,
        owner=request.user,
    )

    send_mailing(mailing)

    return redirect("mailing:list")


def home(request):
    now = timezone.now()

    context = {
        "total_mailings": Mailing.objects.filter(
            owner=request.user
        ).count() if request.user.is_authenticated else 0,

        "active_mailings": Mailing.objects.filter(
            owner=request.user,
            start_time__lte=now,
            end_time__gte=now,
            status=Mailing.STATUS_STARTED,
        ).count() if request.user.is_authenticated else 0,

        "total_recipients": Recipient.objects.filter(
            owner=request.user
        ).count() if request.user.is_authenticated else 0,
    }

    return render(request, "mailing/home.html", context)
