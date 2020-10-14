from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import account_activation_sent, activate, signup
# app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name = 'password_change_done'),
    path('password_reset', auth_views.PasswordResetView.as_view(), name = 'password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('signup/', signup, name='signup'),
]