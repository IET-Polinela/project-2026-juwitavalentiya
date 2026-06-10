from django.urls import path
from .views import dashboard_view, chart_data, report_detail, search_reports

urlpatterns = [
    # DASHBOARD UTAMA
    path('', dashboard_view, name='dashboard'),

    # DATA CHART (API untuk grafik)
    path('chart-data/', chart_data, name='chart_data'),

    # LIVE SEARCH
    path('search/', search_reports, name='dashboard_search'),

    # DETAIL REPORT
    path('detail/<int:report_id>/', report_detail, name='report_detail'),
]