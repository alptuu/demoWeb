from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import OwnerSignUpForm
from .models import Profile


def owner_login(request):
    return render(request, 'owner/login.html')


def owner_registry(request):
    if request.method == 'POST':
        form = OwnerSignUpForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
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