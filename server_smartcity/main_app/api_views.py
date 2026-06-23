from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema # <-- 1. TAMBAHKAN IMPORT INI

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerDraftOrAdmin


class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReportViewSet(viewsets.ModelViewSet):

    queryset = Report.objects.all().order_by('-updated_at')
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ReportPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Report.objects.all().order_by('-updated_at')
        tab = self.request.query_params.get('tab', None)

        if tab == 'my_reports':
            return queryset.filter(reporter=user)

        if tab == 'feed':
            return queryset.exclude(status='DRAFT')

        # default: show non-DRAFT reports and the user's own drafts
        return queryset.filter(
            ~Q(status='DRAFT') | Q(reporter=user)
        )

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    def get_permissions(self):
        permissions = [IsAuthenticated()]

        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsOwnerDraftOrAdmin())

        return permissions

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)