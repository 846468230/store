from rest_framework import serializers
from .models import UserFav
from rest_framework.validators import UniqueTogetherValidator


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),help_text="当前用户id"
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
