from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exams.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^$', login_required(TemplateView.as_view(template_name="home.html"))),
]