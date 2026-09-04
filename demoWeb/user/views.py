from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.core.mail import EmailMessage
from django.conf import settings

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
    ContactMessageForm,
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
        form = OwnerProfileForm(request.POST,request.FILES,user=request.user) # tarayıcıya yüklenmiş dosyaların alımı için "request.FILES" kullanılmalı

        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save(update_fields=['first_name', 'last_name', 'email'])

            profile.biography = form.cleaned_data['biography']
            profile.phone_number = form.cleaned_data['phone_number']

            if form.cleaned_data['cv']:  # dosya seçilmediyse mevcut CV korunur
                profile.cv = form.cleaned_data['cv']

            profile.save(update_fields=['biography', 'phone_number', 'cv'])

            messages.success(request, 'Profil bilgileriniz güncellendi.')
            return redirect('owner_edit')
        else:
            messages.error(request, 'Formda hatalar var, lütfen kontrol edin.')
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

    return render(request, 'owner/edit.html', {'form': form, 'profile': profile})


@login_required
def owner_dashboard(request):
    profile = getattr(request.user, 'profile', None)

    if profile is None or not profile.is_owner:
        raise PermissionDenied

    return render(request, 'owner/dashboard.html')


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
        form = form_class(request.POST,request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, f'{title} eklendi.')
            return redirect('item_list', model_name=model_name)
        else:
            messages.error(request, 'Formda hatalar var, lütfen kontrol edin.')
    else:
        form = form_class()

    return render(request, 'owner/item_form.html', {
        'form': form,
        'title': title,
        'model_name': model_name,
    })


@login_required
def item_update(request, model_name, pk):
    model, form_class, title = _get_item_model(model_name)
    item = get_object_or_404(model, pk=pk, user=request.user)

    if request.method == 'POST':
        form = form_class(request.POST,request.FILES, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, f'{title} güncellendi.')
            return redirect('item_list', model_name=model_name)
        else:
            messages.error(request, 'Formda hatalar var, lütfen kontrol edin.')
    else:
        form = form_class(instance=item)

    return render(request, 'owner/item_form.html', {
        'form': form,
        'title': title,
        'model_name': model_name,
    })


@login_required
def item_delete(request, model_name, pk):
    model, _form_class, title = _get_item_model(model_name)
    item = get_object_or_404(model, pk=pk, user=request.user)

    if request.method == 'POST':
        item.delete()
        messages.success(request, f'{title} silindi.')
        return redirect('item_list', model_name=model_name)

    return render(request, 'owner/item_confirm_delete.html', {
        'item': item,
        'title': title,
        'model_name': model_name,
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    owner = getattr(project.user, 'profile', None)

    return render(request, 'pages/project_detail.html', {'project': project, 'owner': owner})


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    owner = getattr(blog.user, 'profile', None)

    return render(request, 'pages/blog_detail.html', {'blog': blog, 'owner': owner})

@require_POST
def contact_message(request):
    form = ContactMessageForm(request.POST) # HTML formatından gelen verileri "form" nesnesine bağlar 

    if form.is_valid(): # ContactMessageForm'un formatının doğru olup olmadığı kontrol edilir, doğrulama başarılıysa "cleaned_data" üzerinden temizlenmiş ve doğrulanmış veriler alınır
        email_message = EmailMessage(
            subject=f"Portföy iletişim formu: {form.cleaned_data['name']}",
            body=(
                f"Gönderen: {form.cleaned_data['name']}\n"
                f"E-posta: {form.cleaned_data["email"]}\n\n"
                f"Mesaj:\n{form.cleaned_data["message"]}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,  # e-postayı teknik olarak gönderen adres (SMTP hesabıyla aynı olmalı)
            to=[settings.CONTACT_RECIPIENT_EMAIL],  # e-postayı alacak kişilerin adres listesi (tek kişi olsa bile liste olmak zorunda)
            reply_to=[form.cleaned_data["email"]], # formu dolduran ziyaretçinin e-posta adresi 
        )
        email_message.send()
        messages.success(request, 'Mesajınız gönderildi, en kısa sürede dönüş yapılacaktır.')
    else:
        messages.error(request, 'Mesajınız gönderilemedi, lütfen bilgileri kontrol edin.')

    return redirect("/#contact")

def download_cv(request):
    return 











