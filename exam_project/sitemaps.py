from django.contrib.sitemaps import Sitemap
from exams.models import Problem
from django.urls import reverse

class ProblemSitemap(Sitemap):
    def items(self):
        return Problem.objects.all()

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['login', 'register', 'password_reset', 'index', 'preferences', ]

    def location(self, item):
        return reverse(item)