from rest_framework import serializers
from .models import UserFav
from rest_framework.validators import UniqueTogetherValidator
from goods.serializers import CourseFavSerializer
from .models import UserLeavingMessage, UserAddress,UserCourse
import re
from store.settings import REGEX_MOBILE
from datetime import datetime, timedelta


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


class UserCourseSerializer(serializers.Serializer):
    class Meta:
        model = UserCourse
        fields = "__all__"

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
