"""
URL configuration for demoWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render, redirect, get_object_or_404

from user.models import Profile

PLACEHOLDER_TESTIMONIALS = [
    {'quote': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore.', 'name': 'Ayşe Yılmaz', 'role': 'Creative Director'},
    {'quote': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.', 'name': 'Mehmet Demir', 'role': 'Product Manager'},
    {'quote': 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 'name': 'Elif Kaya', 'role': 'Founder, Studio X'},
]

PLACEHOLDER_PARTNERS = ['Acme', 'Northwind', 'Globex', 'Initech', 'Umbrella', 'Soylent']

PLACEHOLDER_POSTS = [
    {'title': 'Tasarım sistemleri neden önemli?', 'excerpt': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'date': '12 Mart 2025', 'image': 'https://picsum.photos/id/180/800/500'},
    {'title': 'Bir ürünü sıfırdan kurgulamak', 'excerpt': 'Sed do eiusmod tempor incididunt ut labore et dolore magna.', 'date': '28 Şubat 2025', 'image': 'https://picsum.photos/id/119/800/500'},
    {'title': 'Kullanıcı araştırmasına giriş', 'excerpt': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco.', 'date': '5 Ocak 2025', 'image': 'https://picsum.photos/id/160/800/500'},
]


def get_owner_profile():
    return Profile.objects.select_related('user').filter(role=Profile.ROLE_OWNER).first()


def main_page(request):
    owner = get_owner_profile()
    context = {
        'owner': owner,
        'testimonials': PLACEHOLDER_TESTIMONIALS,
        'partners': PLACEHOLDER_PARTNERS,
        'posts': PLACEHOLDER_POSTS,
        'stats': {'experience_count': 0, 'project_count': 0, 'course_count': 0, 'skill_count': 0},
    }

    if owner:
        experiences = list(owner.user.experiences.all())
        projects = list(owner.user.projects.all())
        courses = list(owner.user.courses.all())
        skills = list(owner.user.skills.all())
        blogs = list(owner.user.blogs.order_by('-date'))

        context.update({
            'experiences': experiences,
            'projects': projects,
            'educations': owner.user.educations.all(),
            'courses': courses,
            'skills': skills,
            'hobbies': owner.user.hobbies.all(),
            'blogs': blogs,
            'stats': {
                'experience_count': len(experiences),
                'project_count': len(projects),
                'course_count': len(courses),
                'skill_count': len(skills),
            },
        })

    return render(request, 'pages/index.html', context)


def section_redirect(anchor):
    def view(request):
        return redirect('/#' + anchor, permanent=True)

    return view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='home'),
    path('about/', section_redirect('about'), name='about'),
    path('projects/', section_redirect('projects'), name='projects'),
    path('education/', section_redirect('education'), name='education'),
    path('testimonials/', section_redirect('testimonials'), name='testimonials'),
    path('partners/', section_redirect('partners'), name='partners'),
    path('blog/', section_redirect('blog'), name='blog'),
    path('contact/', section_redirect('contact'), name='contact'),
    path('', include('user.urls')),
]

