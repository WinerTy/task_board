from allauth.account import views as allauth_views
from allauth.account.views import EmailVerificationSentView, ConfirmEmailView
from django.urls import path, include
from .views import AboutUs, CustomView, UsersInfo, RoleTools


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('login/', allauth_views.login, name='account_login'),
    path('signup/', CustomView.as_view(), name='account_signup'),
    path('profile/', UsersInfo.profile, name='profile'),
    path('logout/',  allauth_views.logout, name='account_logout'),
    path('password/reset/', allauth_views.password_reset, name='account_reset_password'),
    path('password/change/', allauth_views.password_change, name='account_change_password'),
    path('verification-sent/', EmailVerificationSentView.as_view(), name='account_email_verification_sent'),
    path('confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('accounts/about_us/', AboutUs.show, name='about_us'),
    path('accounts/role/', RoleTools.role, name='role'),
]