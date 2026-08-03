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
from django.shortcuts import redirect, get_object_or_404
from .services import send_mailing


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


def start_mailing(request, pk):

    mailing = get_object_or_404(
        Mailing,
        pk=pk
    )

    send_mailing(mailing)

    return redirect("mailing:list")


from django.shortcuts import render
from django.utils import timezone

from mailing.models import Mailing
from clients.models import Recipient


def home(request):
    now = timezone.now()

    total_mailings = Mailing.objects.count()

    active_mailings = Mailing.objects.filter(
        start_time__lte=now,
        end_time__gte=now,
        status=Mailing.STATUS_STARTED,
    ).count()

    total_recipients = Recipient.objects.count()

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "total_recipients": total_recipients,
    }

    return render(request, "mailing/home.html", context)


from django.utils import timezone
from clients.models import Recipient

class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()

        context["total_mailings"] = Mailing.objects.count()

        context["active_mailings"] = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            status=Mailing.STATUS_STARTED,
        ).count()

        context["total_recipients"] = Recipient.objects.count()

        return context
    