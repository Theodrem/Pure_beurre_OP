from django.urls import path
from django.contrib.auth import views as auth_views

from .views import Register, Login, Dashboard, Logout


urlpatterns = [
    path("register/", Register.as_view(), name='register_view'),
    path("login/", Login.as_view(), name='login_view'),
    path("logout/", Logout.as_view(), name='logout_view'),
    path("dashboard/", Dashboard.as_view(), name='dashboard_view'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='user/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_sent.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_form.html"),name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_done.html"), name='password_reset_complete')
]

