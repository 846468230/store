"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from goods.views import CourseListViewSet, CourseCategoryListView
from users.views import SmsCodeViewset, UserRegViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from utils.weixin import ObtainJSONWechatToken
from user_operation.views import UserFavViewSet
router = DefaultRouter()

# course的url
router.register('courses', CourseListViewSet, basename='courses')
router.register('category', CourseCategoryListView, basename='course-category')
# 手机验证码
router.register('codes', SmsCodeViewset, basename='codes')
# 用户注册
router.register('register', UserRegViewSet, basename="register")
# 微信登录
router.register('login_weixin',ObtainJSONWechatToken,basename="wechat_login")
# 用户收藏
router.register('userfav',UserFavViewSet,basename="userfav")
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('', include(router.urls)),
                  path('docs/', include_docs_urls(title='网站文档')),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  # path('api-token-auth/', views.obtain_auth_token)
                  path('login/', obtain_jwt_token),
                  path('', include('social_django.urls', namespace='social')),
                  #path('login_weixin/',ObtainJSONWechatToken),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
