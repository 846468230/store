from rest_framework import serializers
from .models import UserFav
from rest_framework.validators import UniqueTogetherValidator
from goods.serializers import CourseFavSerializer
from .models import UserLeavingMessage, UserAddress,UserCourse,UserCashWithdrawal
import re
from store.settings import REGEX_MOBILE
from datetime import datetime, timedelta

class UserCashWithdrawSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), help_text="当前用户id"
    )
    apply_status = serializers.CharField(read_only=True)
    withdraw_status = serializers.CharField(read_only=True)
    def validate(self, attrs):
        user = attrs['user']
        apply_category = attrs['apply_category']
        if apply_category == UserCashWithdrawal.WITHDRWAL_CHOICES[0][0]:
            if not user.groups.filter(name="marketer").exists():
                raise serializers.ValidationError("请先成为课程代表，再进行申请")
            if user.user_marketer.commission < attrs['amount']:
                raise serializers.ValidationError("请检查金额后重试")
        elif apply_category == UserCashWithdrawal.WITHDRWAL_CHOICES[1][0]:
            if not user.groups.filter(name="teacher").exists():
                raise serializers.ValidationError("请先申请成为老师，再进行申请")
            if user.teacher_commission.commission < attrs['amount']:
                raise serializers.ValidationError("请检查金额后重试")
        return attrs


    class Meta:
        model = UserCashWithdrawal
        fields = "__all__"

class UserFavListSerializer(serializers.ModelSerializer):
    course = CourseFavSerializer()

    class Meta:
        model = UserFav
        fields = ["course", "id"]


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), help_text="当前用户id"
    )
    added_datetime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    def validate_signer_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """

        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码格式错误")
        return mobile

    class Meta:
        model = UserAddress
        fields = ['user', 'province', "city", "district", "address", "signer_name", "signer_mobile", "added_datetime"]


class UserCourseListSerializer(serializers.Serializer):
    class Meta:
        model = UserCourse
        fields = ["id","user","course"]

class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), help_text="当前用户id"
    )
    added_datetime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ['user', 'message_type', "subject", "message", "file", "added_datetime"]


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), help_text="当前用户id"
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=['user', 'course'],
                message="已经收藏"
            )
        ]
        fields = ["id", "course", "user"]
