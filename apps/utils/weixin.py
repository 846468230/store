#!/usr/bin/env python
# coding=utf-8

from rest_framework_jwt.views import ObtainJSONWebToken

#import emoji as emoji
import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest_framework_jwt.compat import get_username_field
from rest_framework_jwt.settings import api_settings
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin
from rest_framework.response import Response
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from store.settings import WECHAT
import emoji
from rest_framework import status
User = get_user_model()
from rest_framework import views
from django.core.files import File
from io import BytesIO
import time
from urllib.request import urlopen
from users.serializers import GroupSerializer,UserDetailSerializer



class JSONWechatTokenSerializer(serializers.Serializer):
    """
    通过小程序post请求发送code, 经JSONWechatTokenSerializer验证后返回
    openid和session_key.
    使用用户标识openid生成一个user实例, 方便视图对用户权限的管理.
    """

    code = serializers.CharField()
    nickName = serializers.CharField(allow_null=True, )
    gender = serializers.CharField(allow_null=True, )
    language = serializers.CharField(allow_null=True, )
    city = serializers.CharField(allow_null=True, )
    province = serializers.CharField(allow_null=True)
    country = serializers.CharField(allow_null=True, )
    avatarUrl = serializers.CharField(allow_null=True, )

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        code = attrs.get('code')
        result = self._credentials_validation(code)
        user = self._get_or_create_user(result['openid'], result['session_key'])
        r = urlopen(attrs.get('avatarUrl'))
        user.avatar.save("{}_{}.jpg".format(user.id,int(time.time())),File(BytesIO(r.read())))
        attrs['username'] = result['openid']
        attrs['password'] = result['openid']
        self._update_userinfo(user, attrs)
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get( 'password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                if not user.is_active:
                    msg = _('账户未激活')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                data_dict = {
                    'token': jwt_encode_handler(payload),
                    'name': user.name if user.name else user.username,
                    'groups': GroupSerializer(user.groups.all(), many=True).data,
                    'permissions':User.get_all_permissions(user)
                }
                data_dict.update(UserDetailSerializer(user,context=self.context).data)
                attrs.update(data_dict)
                return attrs
            else:
                msg = _('账号或密码不正确')
                raise serializers.ValidationError(msg)
        else:
            msg = _('必须包含用户信息或者code')
            raise serializers.ValidationError(msg)

    @staticmethod
    def _update_userinfo(user, attrs):
        gender = attrs.get('gender')
        gender = 'male' if int(gender) == 1 else 'female'
        User.objects.filter(id=user.id).update(gender=gender,nickname=emoji.demojize(attrs.get('nickName')),)

    @staticmethod
    def _get_or_create_user(openid, session_key):
        user, created = User.objects.get_or_create(
            username=openid,
            openid = openid,
            defaults={'password': openid}
        )
        if created:
            user.set_password(openid)

        user.session_key = session_key
        user.save()
        return user


    @staticmethod
    def _credentials_validation(code):
        # 成功拿到openid和session_key并返回
        req_params = {
            'appid': WECHAT['APPID'],
            'secret': WECHAT['APPSECRET'],
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        url = 'https://api.weixin.qq.com/sns/jscode2session'

        response = requests.get(url, params=req_params)
        result = response.json()

        if 'errcode' in result:
            msg = _(result['errmsg'])
            raise serializers.ValidationError(msg, code='authorization')
        return result


class ObtainJSONWechatToken(views.APIView):
    def post(self,request):
        serializer = JSONWechatTokenSerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_jwt_token = ObtainJSONWechatToken
