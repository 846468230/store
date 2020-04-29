import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import Group, Permission
from rest_framework.validators import UniqueValidator

from .models import VerifyCode

from store.settings import REGEX_MOBILE

User = get_user_model()
"""
当字段比模型多的时候可以使用如下
"""


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionsSerializer(many=True)
    class Meta:
        model = Group
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "name", "avatar", "nickname", "birthday", "gender"]


class UserRegSerializer(serializers.ModelSerializer):
    # 如果会删除code这个属性 那么需要write_only = True 这样返回消息序列化就不回带带着code
    code = serializers.CharField(required=True, write_only=True, max_length=6, min_length=6, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误",
                                 }, help_text="验证码", )
    username = serializers.CharField(label="用户名", help_text="用户名——表单设置为手机号，就不用在输入mobile了，后台逻辑已经改好", required=True,
                                     allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在")])
    password = serializers.CharField(
        style={'input_type': 'password'}, label="密码", help_text="密码", write_only=True
    )

    # 重载了create方法
    def create(self, validated_data):
       user = super(UserRegSerializer,self).create(validated_data=validated_data)
       user.set_password(validated_data["password"])
       user.save()
       return user

    def validate_code(self, code):
        """
        单独验证code字段
        :param code:
        :return:
        """
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-added_datetime")
        if verify_records:
            last_record = verify_records[0]
            twenty_minutes_ago = datetime.now() - timedelta(hours=0, minutes=20, seconds=0)
            if twenty_minutes_ago > last_record.added_datetime:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ["username", "password", "code", "mobile"]


"""
当某些字段比模型少，切必须输入时，前端没传入，从后端生成时可以使用这个
"""


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, help_text="手机号码")

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("该手机号码已经被注册")

        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(added_datetime__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上次发送未超过60s")

        return mobile
