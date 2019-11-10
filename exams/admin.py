from django.contrib import admin
from exams.models import *
from django.db.models import Q

admin.site.site_header = "Példatár Alkalmazás"
admin.site.site_title = "Példatár Alkalmazás"

class TagInline(admin.TabularInline):
    model = Problem.tags.through
    extra = 3

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
    
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['creator', 'title', 'short_description']
    inlines = [HintInline]
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change): 
        obj.creator = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(ProblemAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(creator=request.user)

admin.site.register(Tag)
admin.site.register(Skill)
admin.site.register(Level)
admin.site.register(Author)
admin.site.register(Place)
admin.site.register(Publisher)
admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Citation, CitationAdmin)
admin.site.register(PythonLibrary, PythonLibraryAdmin)
