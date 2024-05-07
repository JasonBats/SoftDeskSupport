from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

from SoftDeskApp.models import Contributor


class IsAdminAuthenticated(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


class IsStaffAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class IsProjectContributorAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if request.method == 'POST':
            project_contributors = [user.user_id for user in
                                    Contributor.objects.filter(
                                        project_id=request.data['project'])]
            if request.user.id in project_contributors:
                return True
            else:
                raise PermissionDenied('Vous devez être contributeur'
                                       ' de ce projet pour faire cela.')
        return True


class IsRightUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class CanManageProjectContributors(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            contributing_to = [project.project_id for project in Contributor.objects.filter(user_id=request.user.id)]
            if obj.project.id in contributing_to:
                return True
            else:
                raise PermissionDenied('Vous devez être contributeur'
                                       ' de ce projet pour faire cela.')
        elif request.method in SAFE_METHODS:
            return request.user.is_authenticated
