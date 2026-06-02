from rest_framework.permissions import BasePermission


class IsOwnerAndDraft(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in ['PUT', 'PATCH', 'DELETE']:

            return (
                obj.reporter == request.user
                and obj.status == 'DRAFT'
            )

        return True