from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.contrib.auth import get_user_model
from users.serializers import GroupSerializer, UserDetailSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer, RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer
)

User = get_user_model()
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class jsonwebtokenapiview(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response_data.update(UserDetailSerializer(user).data)
            response_data["groups"] = GroupSerializer(user.groups.all(), many=True).data
            response_data["permissions"] = sorted( User.get_all_permissions(user))
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainJSONWebToken(jsonwebtokenapiview):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()
