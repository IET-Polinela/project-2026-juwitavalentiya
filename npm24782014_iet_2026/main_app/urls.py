from django.urls import path
from .views import (
    ReportListView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
    report_stats_api,
    search_reports,
    report_detail_api,
)

urlpatterns = [

    # REPORT MANAGEMENT
    path('', ReportListView.as_view(), name='report_list'),
    path('add/', ReportCreateView.as_view(), name='report_add'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='report_edit'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),
    path('status/<int:pk>/', ReportUpdateStatusView.as_view(), name='report_status_update'),

    # APIs
    path('chart-data/', report_stats_api, name='report_stats_api'),
    path('search/', search_reports, name='report_search_api'),
    path('api/detail/<int:pk>/', report_detail_api, name='report_detail'),

]