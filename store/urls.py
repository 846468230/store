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
from goods.views import CourseListViewSet, CourseCategoryListView,BannerListViewSet,LessonRetrieveViewSet
from users.views import SmsCodeViewset, UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
#from rest_framework_jwt.views import obtain_jwt_token
from utils.JSONWebTokenAPIView import obtain_jwt_token
from utils.weixin import ObtainJSONWechatToken
from trade.views import ShoppingCartViewSet,OrderViewset,AlipayView
from user_operation.views import UserFavViewSet,UserLeavingMessageViewSet,UserAddressViewSet,UserCourseViewSet,UserCashWithDrawViewSet
from marketing.views import MarketingRelationshipViewSet,PosterViewSet,TeacherApplicationViewSet,MarketerApplicationViewSet,MarketingCodeViewSet
from trade.views import TeacherManagementViewSet
router = DefaultRouter()

# course的url
router.register('courses', CourseListViewSet, basename='courses')
router.register('category', CourseCategoryListView, basename='course-category')
# 手机验证码
router.register('codes', SmsCodeViewset, basename='codes')
# 用户注册
router.register('user', UserViewSet, basename="register")
# 微信登录
#router.register('login_weixin',ObtainJSONWechatToken,basename="wechat_login")
# 用户收藏
router.register('userfav',UserFavViewSet,basename="userfav")
# 用户留言
router.register('leaving_message',UserLeavingMessageViewSet,basename="leaving_message")
# 用户地址
router.register('address',UserAddressViewSet,basename="address")
# 购物车
router.register('shoppingcart',ShoppingCartViewSet,basename="shoppingcart")
# 订单信息
router.register('order',OrderViewset,basename="order")
# 轮播图
router.register('banner',BannerListViewSet,basename="banner")
# 课程页面
router.register('lesson',LessonRetrieveViewSet,basename="lesson")
# 用户购买的课程
router.register('user_course',UserCourseViewSet,basename="user_course")
# 用户的营销关系
router.register('marketing',MarketingRelationshipViewSet,basename="marketing")
# 海报
router.register('poster',PosterViewSet,basename="poster")
# 老师身份申请
router.register('teacher_application',TeacherApplicationViewSet,basename='teacher_application')
# 营销人员身份申请
router.register('marketer_application',MarketerApplicationViewSet,basename="marketer_application")
# 老师佣金
router.register('teacher_commission',TeacherManagementViewSet,basename="teacher_commission")
# 营销推广码
router.register('marketing_code',MarketingCodeViewSet,basename='marketing_code')
# 提现申请
router.register('cash_withdraw',UserCashWithDrawViewSet,basename="cash_withdraw")
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('', include(router.urls)),
                  path('docs/', include_docs_urls(title='网站文档')),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  # path('api-token-auth/', views.obtain_auth_token)
                  path('login/', obtain_jwt_token),
                  path('alipay/return/',AlipayView.as_view()),
                  path('', include('social_django.urls', namespace='social')),
                  path('login_weixin/',ObtainJSONWechatToken.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
