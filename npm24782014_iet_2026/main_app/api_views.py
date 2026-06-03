from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraft


class ReportViewSet(viewsets.ModelViewSet):

    queryset = Report.objects.all()

    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, "is_admin") and user.is_admin:
            return Report.objects.all()

        return Report.objects.filter(reporter=user)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    def get_permissions(self):
        permissions = [IsAuthenticated()]

        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsOwnerAndDraft())

        return permissions