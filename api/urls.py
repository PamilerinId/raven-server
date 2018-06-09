from django.conf.urls import url, include
from rest_framework import routers
import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = routers.DefaultRouter()

router.register(r'payees', views.PayeeViewSet)
router.register(r'fees', views.FeeViewSet)
router.register(r'user-list', views.UserListDetailView)
router.register(r'user', views.UserProfileAPIView)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    url(r'^login/$', views.UserLoginAPIView.as_view(), name='login'),
    url(r'register/$', views.UserRegistrationAPIView.as_view(), name='register'),
    url(r'^auth-login/$', obtain_jwt_token, name='get_token'),
    url(r'^token-verify/$', verify_jwt_token, name='verify_token'),
    url(r'^token-refresh/$', refresh_jwt_token, name='refresh_token'),
    url(r'^', include(router.urls)),

]