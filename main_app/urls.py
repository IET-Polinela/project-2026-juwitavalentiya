from django.urls import path
from .views import *

urlpatterns = [

    # DASHBOARD
    path(
        '',
        dashboard_view,
        name='dashboard'
    ),

    # CHART API
    path(
        'chart-data/',
        report_stats_api,
        name='report_stats_api'
    ),

    # SEARCH API
    path(
        'search/',
        search_reports,
        name='report_search_api'
    ),

    # DETAIL MODAL API
    path(
        'api/detail/<int:pk>/',
        report_detail_api,
        name='report_detail'
    ),

]