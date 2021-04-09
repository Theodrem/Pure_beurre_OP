from django.urls import path
from .views import Register, Login, Dashboard, Logout

urlpatterns = [
    path("register/", Register.as_view(), name='register_view'),
    path("login/", Login.as_view(), name='login_view'),
    path("logout/", Logout.as_view(), name='logout_view'),
    path("dashboard/", Dashboard.as_view(), name='dashboard_view')
]