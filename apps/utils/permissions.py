from rest_framework import permissions
from user_operation.models import UserCourse
from goods.models import Course


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class boughtOrOwnerOrAdmin(permissions.BasePermission):
    message = '您还没有购买该课程'

    def is_admin(user):
        return user.groups.filter(name="admin").exists()

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if not request.user.is_active:
            return False
        return boughtOrOwnerOrAdmin.is_admin(request.user) or UserCourse.objects.filter(
            course=obj.course).exists() or Course.objects.filter(teacher=request.user)
