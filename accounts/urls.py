from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    login_view,
    register_view,
    logout_view
)

urlpatterns = [
    url(r"^login/$", login_view, name = "login"),
    url(r"^register/$", register_view, name = "register"),
    url(r'^logout/$', logout_view, name = "logout"),
    path('reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]