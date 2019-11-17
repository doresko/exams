from django.contrib.sitemaps import Sitemap
from exams.models import Problem
from django.urls import reverse

class ProblemSitemap(Sitemap):
    priority = 1

    def items(self):
        return Problem.objects.all()

class StaticViewSitemap(Sitemap):
    priority = 0.8

    def items(self):
        return ['login', 'register', 'index', 'preferences', ]

    def location(self, item):
        return reverse(item)