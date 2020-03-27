from rest_framework import serializers
from .models import MarketingRelationship, Poster, TeacherApplication, MarketerApplication,MarketingCode
from django.contrib.auth import get_user_model

User = get_user_model()


class MarketingCodeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), help_text="当前用户id"
    )
    code = serializers.CharField(read_only=True)
    def generate_code(self):
        # 当前时间+userid+随机数
        from random import Random
        import time
        random_ins = Random()
        code = "{time_str}{ranstr}{userid}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))

        return code

    def validate(self, attrs):
        attrs['code'] = self.generate_code()
        return attrs

    class Meta:
        model = MarketingCode
        fields = "__all__"

class MarketUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "name", "nickname", "avatar", "birthday", "gender"]


class MaketerSubUserSerializer(serializers.ModelSerializer):
    user = MarketUserSerializer(many=False)

    class Meta:
        model = MarketingRelationship
        fields = ["user"]


class UserAndSubMarketerSerializer(serializers.ModelSerializer):
    sub_marketer = MaketerSubUserSerializer(many=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "name", "nickname", "avatar", "birthday", "gender", "sub_marketer"]


class MarketingRelationshipSerializer(serializers.ModelSerializer):
    user = UserAndSubMarketerSerializer(many=False)
    parent_marketer = MarketUserSerializer(many=False)

    class Meta:
        fields = "__all__"
        model = MarketingRelationship


class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Poster


class TeacherApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), help_text="当前用户id"
    )
    apply_status = serializers.CharField(read_only=True)

    class Meta:
        fields = "__all__"
        model = TeacherApplication


class MarketerApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), help_text="当前用户id"
    )
    apply_status = serializers.CharField(read_only=True)

    class Meta:
        fields = "__all__"
        model = MarketerApplication
