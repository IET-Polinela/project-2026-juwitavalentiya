from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count

from main_app.models import Report


def dashboard_view(request):

    # DATA STATUS
    status_data = list(
        Report.objects.values('status')
        .annotate(total=Count('id'))
    )

    # DATA CATEGORY
    category_data = list(
        Report.objects.values('category')
        .annotate(total=Count('id'))
    )

    # 5 REPORTED
    latest_reports = Report.objects.filter(
        status='REPORTED'
    )[:5]

    # 5 RESOLVED
    resolved_reports = Report.objects.filter(
        status='RESOLVED'
    )[:5]

    # SEMUA LAPORAN
    all_reports = Report.objects.all()

    context = {
        'status_data': status_data,
        'category_data': category_data,
        'latest_reports': latest_reports,
        'resolved_reports': resolved_reports,
        'all_reports': all_reports,
    }

    return render(
        request,
        'dashboard/index.html',
        context
    )


# CHART DATA
def chart_data(request):

    data = list(
        Report.objects.values('status')
        .annotate(total=Count('id'))
    )

    return JsonResponse(data, safe=False)


# DETAIL MODAL
def report_detail(request, report_id):

    report = Report.objects.get(id=report_id)

    data = {
        'title': report.title,
        'category': report.category,
        'status': report.status,
        'description': report.description,
        'location': report.location,
    }

    return JsonResponse(data)