from rest_framework import permissions
from user_operation.models import UserCourse,UserCashWithdrawal
from marketing.models import MarketingRelationship
from trade.models import TeacherManagement
from django.contrib.auth.models import Group
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


class teacherOrmarketerAndEnough(permissions.BasePermission):
    message = '请确认您是否是导师或营销人员，且账户中佣金数目充足'

    def has_object_permission(self, request, view, obj):
        return True
        user = obj.user
        apply_category = obj.apply_category
        if apply_category == UserCashWithdrawal.WITHDRWAL_CHOICES[0][0]:
            if not user.groups.filter(name="marketer").exists():
                return False
            if user.user_marketer.commission < obj.amount:
                return False
            return True
        elif apply_category == UserCashWithdrawal.WITHDRWAL_CHOICES[1][0]:
            if not user.groups.filter(name="teacher").exists():
                return False
            if user.teacher_commission.commission < obj.amount:
                return False
            return True
        else:
            return False