from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Report
from .forms import ReportForm

# =========================================
# ADDED FOR LAB 14: OPENAPI UTILS
# =========================================
from drf_spectacular.utils import extend_schema


# =========================================
# HOME / REPORT LIST
# =========================================
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_reports'] = Report.objects.count()
        context['reported_count'] = Report.objects.filter(status='REPORTED').count()
        context['verified_count'] = Report.objects.filter(status='VERIFIED').count()
        context['in_progress_count'] = Report.objects.filter(status='IN_PROGRESS').count()
        context['resolved_count'] = Report.objects.filter(status='RESOLVED').count()
        return context


# =========================================
# DASHBOARD PAGE
# =========================================
def dashboard_view(request):

    recent_reports = Report.objects.order_by('-id')[:5]

    resolved_reports = Report.objects.filter(
        status='DONE'
    ).order_by('-id')[:5]

    context = {
        'recent_reports': recent_reports,
        'resolved_reports': resolved_reports,
    }

    return render(
        request,
        'main_app/dashboard.html',
        context
    )


# =========================================
# DASHBOARD CHART DATA API
# =========================================
def report_stats_api(request):

    # STATUS
    status_data = Report.objects.values(
        'status'
    ).annotate(
        total=Count('id')
    )

    status_labels = []
    status_values = []

    for item in status_data:
        status_labels.append(item['status'])
        status_values.append(item['total'])

    # CATEGORY
    category_data = Report.objects.values(
        'category'
    ).annotate(
        total=Count('id')
    )

    category_labels = []
    category_values = []

    for item in category_data:
        category_labels.append(item['category'])
        category_values.append(item['total'])

    data = {
        'status_labels': status_labels,
        'status_data': status_values,
        'category_labels': category_labels,
        'category_data': category_values,
    }

    return JsonResponse(data)


# =========================================
# LIVE SEARCH API
# =========================================
def search_reports(request):

    query = request.GET.get('q', '')

    reports = Report.objects.filter(
        title__icontains=query
    )[:10]

    data = {
        'reports': [
            {
                'id': r.id,
                'title': r.title,
                'status': r.status,
                'category': r.category,
            }
            for r in reports
        ]
    }

    return JsonResponse(data)


# =========================================
# DETAIL MODAL API
# =========================================
@extend_schema(exclude=True)
def report_detail_api(request, pk):

    report = get_object_or_404(
        Report,
        pk=pk
    )

    data = {
        "id": report.id,
        "title": report.title,
        "description": report.description,
        "status": report.status,
        "location": report.location,
        "category": report.category,
        "created_at": str(report.created_at),
    }

    return JsonResponse(data)


# =========================================
# CREATE REPORT
# =========================================
class ReportCreateView(LoginRequiredMixin, CreateView):

    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_admin:
            messages.error(
                request,
                "❌ Hanya admin yang bisa menambah laporan!"
            )
            return redirect('report_list')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):

        messages.success(
            self.request,
            "✅ Laporan berhasil ditambahkan"
        )

        return super().form_valid(form)


# =========================================
# UPDATE REPORT
# =========================================
class ReportUpdateView(LoginRequiredMixin, UpdateView):

    model = Report
    form_class = ReportForm
    template_name = 'main_app/edit_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_admin:
            messages.error(
                request,
                "❌ Tidak punya akses edit!"
            )
            return redirect('report_list')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):

        messages.success(
            self.request,
            "✅ Laporan berhasil diupdate"
        )

        return super().form_valid(form)


# =========================================
# DELETE REPORT
# =========================================
class ReportDeleteView(LoginRequiredMixin, DeleteView):

    model = Report
    template_name = 'main_app/delete_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_admin:
            messages.error(
                request,
                "❌ Tidak punya akses hapus!"
            )
            return redirect('report_list')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def delete(self, request, *args, **kwargs):

        messages.success(
            self.request,
            "🗑️ Laporan berhasil dihapus"
        )

        return super().delete(
            request,
            *args,
            **kwargs
        )


# =========================================
# UPDATE STATUS
# =========================================
class ReportUpdateStatusView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_admin:
            messages.error(
                request,
                "❌ Tidak punya akses ubah status!"
            )
            return redirect('report_list')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def post(self, request, pk):

        report = get_object_or_404(
            Report,
            pk=pk
        )

        report.status = request.POST.get('status')
        report.save()

        messages.success(
            request,
            "🔄 Status berhasil diperbarui"
        )

        return redirect('report_list')