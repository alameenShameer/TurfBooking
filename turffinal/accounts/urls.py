from django.urls import path
from .views import (
    login_view,
    logout_view,
    admin_dashboard,
    turf_dashboard,
    user_dashboard,
    user_signup,
    owner_signup,
)


urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("admin/", admin_dashboard, name="admin_dashboard"),
    path('turf-dashboard/', turf_dashboard, name='turf_dashboard'),
    path("user/", user_dashboard, name="user_dashboard"),
    path('signup/user/', user_signup, name='user_signup'),
    path('signup/owner/', owner_signup, name='owner_signup'),

]
