import datetime
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify

class Tag(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete = models.PROTECT)
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return(self.name)
  
class PythonLibrary(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete = models.PROTECT)
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=1024)
    url = models.TextField(max_length=256)

    class Meta:
        verbose_name_plural = 'Python libraries'

    def __str__(self):
        return(self.name)

class Skill(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete = models.PROTECT)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return(self.name)

class Level(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete = models.PROTECT)
    name = models.CharField(max_length=64, unique=True, default="")

    def __str__(self):
        return(self.name)

#Publications
class Author(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete = models.PROTECT)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return(self.name)

class Publisher(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete = models.PROTECT)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return(self.name)

class Place(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete = models.PROTECT)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return(self.name)

class Citation(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete = models.PROTECT)
    authors = models.ManyToManyField(Author, help_text='Szerzők')
    title = models.TextField(max_length=256)
    publisher = models.ForeignKey(Publisher, on_delete = models.PROTECT, blank=True, null=True)
    place = models.ForeignKey(Place, on_delete = models.PROTECT, blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    url = models.TextField(max_length=256, blank=True, null=True)
    other = models.TextField(max_length=1024, blank=True, null=True)

    def __str__(self):
        authors = " – ".join(str(authors) for authors in self.authors.all())
        return '{}: {} {} {} {}'.format(authors, self.title, self.place or "", self.publisher or "", self.year or "")

#This is the main entity: a programming problem
class Problem(MPTTModel):
    creator = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete = models.CASCADE)
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete = models.PROTECT, null = True, blank = True, related_name = 'children')
    levels = models.ManyToManyField(Level, help_text = 'Milyen tudásszintű hallgatóknak ajánljuk a feladatot')
    tags = models.ManyToManyField(Tag, help_text = 'Általános tag-ek, amelyekkel keresni lehet, pl. téma, jelleg, stb.')
    skills = models.ManyToManyField(Skill, help_text='Készségek, melyeket a feladat fejleszt. ')
    recommended_libraries = models.ManyToManyField(PythonLibrary, help_text = 'A feladat megoldásához javasolt programkönyvtárak.', blank=True)
    sources = models.ManyToManyField(Citation)
    short_description = models.TextField()
    full_description = models.TextField()
    solution_code = models.TextField()
    solution_explanation = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['id']

    def __str__(self):
        return(self.title)

    def get_absolute_url(self):
        return reverse('task', args=[str(self.slug)])

class Hint(models.Model):
    problem = models.ForeignKey(Problem, on_delete = models.CASCADE)
    priority = models.PositiveSmallIntegerField(help_text = "Sorszám: hányadikként jelenjen meg a segítség")
    hint = models.CharField(max_length=256)
    explanation = models.TextField(null=True, blank=True)

    def __str__(self):
        return(self.hint)

class Snippet(models.Model):
    user = models.ForeignKey(User, null=True, editable=False, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, null=True, editable=False, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return '{}: {}'.format(self.user, self.problem)
