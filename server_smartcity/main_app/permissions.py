from rest_framework.permissions import BasePermission


class IsOwnerDraftOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in ['PUT', 'PATCH']:
            if request.user.is_superuser or getattr(request.user, 'is_admin', False):
                return True

            return obj.reporter == request.user and obj.status == 'DRAFT'

        if request.method == 'DELETE':
            return obj.reporter == request.user and obj.status == 'DRAFT'

        return True