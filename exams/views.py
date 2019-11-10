from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Problem, Hint, Snippet, Tag, Skill
from django.db.models import Q
from .forms import SnippetForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def searchlist(request):
    problems = Problem.objects.all()
    query = request.GET.get('q')
    if query:
        problems = Problem.objects.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(problems, 10)
    page = request.GET.get('page')

    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    context = {
        'object_list': object_list
    }
    return render(request, "search_results.html", context)

def index(request):
    problems = Problem.objects.order_by('id')
    tags = Tag.objects.all()
    skills = Skill.objects.all()
    paginator = Paginator(problems, 10)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    return render(request, 'home.html', {
        'object_list': object_list,
        'tags' : tags,
        'skills' : skills,
        })

def task(request, problem_slug):
    problem = get_object_or_404(Problem, slug=problem_slug)
    problem_id = Problem.objects.only('id').get(slug=problem_slug).id
    hints = Hint.objects.filter(problem = problem_id)
    family = Problem.objects.get(slug=problem_slug).get_family()
    
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.problem=problem
            instance.save()
    else:
        form = SnippetForm()
    return render(request, "detail.html", {
        'problem': problem,
        'hints': hints,
        'family' : family,
        'form': form,
    })

def preferences(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sikeres jelszócsere')
            return redirect('preferences')
        else:
            messages.error(request, 'Sikertelen jelszócsere')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'preferences.html', {
        'form': form,
    })