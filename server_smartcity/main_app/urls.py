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
    home_view,
)

urlpatterns = [

    # HALAMAN PUBLIK
    path('home/', home_view, name='home'),

    # REPORT MANAGEMENT (ADMIN) - tiap view diberi 2 nama (alias)
    path('', ReportListView.as_view(), name='report_list'),
    path('reports/', ReportListView.as_view(), name='reports_list'),

    path('add/', ReportCreateView.as_view(), name='report_add'),
    path('add/', ReportCreateView.as_view(), name='add_report'),

    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='report_edit'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='update_report'),

    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),

    path('status/<int:pk>/', ReportUpdateStatusView.as_view(), name='report_status_update'),
    path('status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_status'),
    path('status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_report_status'),

    # APIs / UTILITAS
    path('chart-data/', report_stats_api, name='report_stats_api'),

    path('search/', search_reports, name='report_search_api'),
    path('search/', search_reports, name='report_search'),

    path('api/detail/<int:pk>/', report_detail_api, name='report_detail'),

]