from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    BlogForm,
    ContactForm,
    CourseForm,
    EducationForm,
    ExperienceForm,
    OwnerLoginForm,
    OwnerProfileForm,
    OwnerSignUpForm,
    ProjectForm,
    SkillForm,
)
from .models import Blog, Contact, Course, Education, Experience, Profile, Project, Skill


def owner_login(request):
    if request.method == 'POST':
        form = OwnerLoginForm(request, data=request.POST) 

        if form.is_valid():
            login(request, form.get_user())
            return redirect('owner_edit')
    else:
        form = OwnerLoginForm()

    return render(request, 'owner/login.html', {'form': form})


@login_required
def owner_logout(request):
    logout(request)
    return redirect('home')


def owner_registry(request):
    if request.method == 'POST':
        form = OwnerSignUpForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'], 
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password=form.cleaned_data['password'],
                )

                Profile.objects.create(
                    user=user,
                    role=Profile.ROLE_OWNER,
                )

            login(request, user)
            return redirect('home')
    else:
        form = OwnerSignUpForm()

    return render(request, 'owner/registry.html', {'form': form})


@login_required
def owner_edit(request):
    profile = getattr(request.user, 'profile', None)

    if profile is None or not profile.is_owner:
        raise PermissionDenied

    if request.method == 'POST':
        form = OwnerProfileForm(request.POST, user=request.user)

        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save(update_fields=['first_name', 'last_name', 'email'])

            profile.biography = form.cleaned_data['biography']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.save(update_fields=['biography', 'phone_number'])

            return redirect('owner_edit')
    else:
        form = OwnerProfileForm(
            user=request.user,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'biography': profile.biography,
                'phone_number': profile.phone_number,
            },
        )

    return render(request, 'owner/edit.html', {'form': form})


# model_name (URL) -> (model, form, başlık) eşlemesi; CRUD view'ları bunu paylaşır
ITEM_MODELS = {
    'experience': (Experience, ExperienceForm, 'Deneyim'),
    'project': (Project, ProjectForm, 'Proje'),
    'education': (Education, EducationForm, 'Eğitim'),
    'course': (Course, CourseForm, 'Kurs'),
    'skill': (Skill, SkillForm, 'Yetenek'),
    'blog': (Blog, BlogForm, 'Blog Yazısı'),
    'contact': (Contact, ContactForm, 'İletişim'),
}


def _get_item_model(model_name):
    try:
        return ITEM_MODELS[model_name]
    except KeyError:
        raise Http404


@login_required
def item_list(request, model_name):
    model, _form_class, title = _get_item_model(model_name)
    items = model.objects.filter(user=request.user)

    return render(request, 'owner/item_list.html', {
        'items': items,
        'model_name': model_name,
        'title': title,
    })


@login_required
def item_create(request, model_name):
    model, form_class, title = _get_item_model(model_name)

    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('item_list', model_name=model_name)
    else:
        form = form_class()

    return render(request, 'owner/item_form.html', {'form': form, 'title': title})


@login_required
def item_update(request, model_name, pk):
    model, form_class, title = _get_item_model(model_name)
    item = get_object_or_404(model, pk=pk, user=request.user)

    if request.method == 'POST':
        form = form_class(request.POST, instance=item)

        if form.is_valid():
            form.save()
            return redirect('item_list', model_name=model_name)
    else:
        form = form_class(instance=item)

    return render(request, 'owner/item_form.html', {'form': form, 'title': title})


@login_required
def item_delete(request, model_name, pk):
    model, _form_class, title = _get_item_model(model_name)
    item = get_object_or_404(model, pk=pk, user=request.user)

    if request.method == 'POST':
        item.delete()
        return redirect('item_list', model_name=model_name)

    return render(request, 'owner/item_confirm_delete.html', {'item': item, 'title': title})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    owner = getattr(project.user, 'profile', None)

    return render(request, 'pages/project_detail.html', {'project': project, 'owner': owner})


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    owner = getattr(blog.user, 'profile', None)

    return render(request, 'pages/blog_detail.html', {'blog': blog, 'owner': owner})








