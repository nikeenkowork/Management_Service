from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from clients.models import Recipient

from .forms import MailingForm
from .models import Mailing, MailingAttempt
from .services import send_mailing


CACHE_TIMEOUT = 300


def clear_user_cache(user_id):
    cache.delete(f"home_stats_user_{user_id}")
    cache.delete(f"statistics_user_{user_id}")


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

        cache_key = f"home_stats_user_{self.request.user.id}"

        statistics = cache.get(cache_key)

        if statistics is None:
            now = timezone.now()

            statistics = {
                "total_mailings": Mailing.objects.filter(
                    owner=self.request.user
                ).count(),

                "active_mailings": Mailing.objects.filter(
                    owner=self.request.user,
                    start_time__lte=now,
                    end_time__gte=now,
                    status=Mailing.STATUS_STARTED,
                ).count(),

                "total_recipients": Recipient.objects.filter(
                    owner=self.request.user
                ).count(),
            }

            cache.set(
                cache_key,
                statistics,
                CACHE_TIMEOUT,
            )

        context.update(statistics)

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

        clear_user_cache(self.request.user.id)

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

        clear_user_cache(self.request.user.id)

        return response


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:list")

    def get_queryset(self):
        return Mailing.objects.filter(
            owner=self.request.user
        )

    def form_valid(self, form):
        response = super().form_valid(form)

        clear_user_cache(self.request.user.id)

        return response


def start_mailing(request, pk):
    mailing = get_object_or_404(
        Mailing,
        pk=pk,
        owner=request.user,
    )

    send_mailing(mailing)

    clear_user_cache(request.user.id)

    return redirect("mailing:list")


def home(request):
    if request.user.is_authenticated:
        cache_key = f"home_stats_user_{request.user.id}"

        statistics = cache.get(cache_key)

        if statistics is None:
            now = timezone.now()

            statistics = {
                "total_mailings": Mailing.objects.filter(
                    owner=request.user
                ).count(),

                "active_mailings": Mailing.objects.filter(
                    owner=request.user,
                    start_time__lte=now,
                    end_time__gte=now,
                    status=Mailing.STATUS_STARTED,
                ).count(),

                "total_recipients": Recipient.objects.filter(
                    owner=request.user
                ).count(),
            }

            cache.set(
                cache_key,
                statistics,
                CACHE_TIMEOUT,
            )

    else:
        statistics = {
            "total_mailings": 0,
            "active_mailings": 0,
            "total_recipients": 0,
        }

    return render(
        request,
        "mailing/home.html",
        statistics,
    )


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "mailing/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cache_key = f"statistics_user_{self.request.user.id}"

        statistics = cache.get(cache_key)

        if statistics is None:
            attempts = MailingAttempt.objects.filter(
                mailing__owner=self.request.user
            )

            statistics = {
                "total_sent": attempts.count(),

                "successful": attempts.filter(
                    status=MailingAttempt.STATUS_SUCCESS
                ).count(),

                "failed": attempts.filter(
                    status=MailingAttempt.STATUS_FAILED
                ).count(),
            }

            cache.set(
                cache_key,
                statistics,
                CACHE_TIMEOUT,
            )

        context.update(statistics)

        return context
