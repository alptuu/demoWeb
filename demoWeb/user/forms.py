from django import forms
from django.contrib.auth.models import User


class OwnerSignUpForm(forms.Form):
    first_name = forms.CharField(
        label="Ad",
        max_length=150,
    )
    last_name = forms.CharField(
        label="Soyad",
        max_length=150,
    )
    email = forms.EmailField(
        label="E-posta",
    )
    password = forms.CharField(
        label="Şifre",
        widget=forms.PasswordInput,
        min_length=8,
    )
    password_confirm = forms.CharField(
        label="Şifre Tekrarı",
        widget=forms.PasswordInput,
        min_length=8,
    )

    def clean_email(self): #django'nun kendi User modelinde email alanı benzersiz değildir (birden fazla kullanıcı aynı email ile kayıt olabilir) 
        # fakat bu durum "clean_email" metoduyla kontrol ediliyor
        email = self.cleaned_data["email"]

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Bu e-posta adresi zaten kullanılıyor."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                "Şifreler birbiriyle aynı değil."
            )

        return cleaned_data





