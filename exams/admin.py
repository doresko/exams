from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib import admin
from exams.models import *
from django.db.models import Q

admin.site.site_header = "Példatár Alkalmazás"
admin.site.site_title = "Példatár Alkalmazás"

class PythonLibraryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'url']

class CitationAdmin(admin.ModelAdmin):
    list_display = ['get_authors', 'title', 'publisher', 'place', 'year']

    def get_authors(self, obj):
        return ", ".join([a.name for a in obj.authors.all()])

class SnippetAdmin(admin.ModelAdmin):
    list_display = ['user', 'problem', 'created_at']
    list_filter = (
        ('problem', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
        'created_at',
    )
    list_select_related = (
        'user',
        'problem'
    )

    def get_queryset(self, request):
        qs = super(SnippetAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return Snippet.objects.select_related('problem').filter(problem__creator=request.user)

class HintInline(admin.TabularInline):
    model=Hint
    extra=1

class OwnerFilter(SimpleListFilter):
    title = 'Saját feladatok'
    parameter_name = 'feladat'

    def lookups(self, request, model_admin):
        return [
            ('own', 'Saját'),
        ] 

    def queryset(self, request, obj):
        if self.value() == 'own':
            return Problem.objects.filter(creator=request.user)
    
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['creator', 'title', 'short_description']
    inlines = [HintInline]
    prepopulated_fields = {'slug': ('title',)}
    list_filter = (OwnerFilter, )


    def save_model(self, request, obj, form, change): 
        obj.creator = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj is not None and obj.creator != request.user:
                return False
            return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.creator != request.user:
            return False
        return True


class TagAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj is not None and obj.creator != request.user:
                return False
            return True

class SkillAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj is not None and obj.creator != request.user:
                return False
            return True

class LevelAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj is not None and obj.creator != request.user:
                return False
            return True

class AuthorAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj is not None and obj.creator != request.user:
                return False
            return True

class PlaceAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj is not None and obj.creator != request.user:
                return False
            return True

class PublisherAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj is not None and obj.creator != request.user:
                return False
            return True

admin.site.register(Tag, TagAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Citation, CitationAdmin)
admin.site.register(PythonLibrary, PythonLibraryAdmin)
