from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin,RetrieveModelMixin
from rest_framework import viewsets
# Create your views here.
from .serializers import UserFavSerializer
from .models import UserFav
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(CreateModelMixin, ListModelMixin,RetrieveModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    """
    用户收藏
    """
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = UserFavSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "course_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
