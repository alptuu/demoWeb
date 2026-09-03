from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Course, Education, Experience, Project, Skill, Blog, Contact


class OwnerLoginForm(AuthenticationForm):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput)


class OwnerSignUpForm(forms.Form):
    username = forms.CharField(
        label="Kullanıcı Adı",
        max_length=150,
    )
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


class OwnerProfileForm(forms.Form):
    first_name = forms.CharField(label="Ad", max_length=150)
    last_name = forms.CharField(label="Soyad", max_length=150)
    email = forms.EmailField(label="E-posta")
    biography = forms.CharField(
        label="Biyografi",
        widget=forms.Textarea,
        required=False,
    )
    phone_number = forms.CharField(
        label="Telefon Numarası",
        max_length=20,
        required=False,
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user #email benzersizlik kontrolünde kullanıcının kendi kaydını hariç tutmak için
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]
        query = User.objects.filter(email__iexact=email)

        if self.user is not None:
            query = query.exclude(pk=self.user.pk)

        if query.exists():
            raise forms.ValidationError(
                "Bu e-posta adresi zaten kullanılıyor."
            )

        return email


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "company", "start_date", "end_date"]
        labels = {
            "title": "Başlık",
            "description": "Açıklama",
            "company": "Şirket",
            "start_date": "Başlangıç Tarihi",
            "end_date": "Bitiş Tarihi",
        }
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "url"]
        labels = {
            "title": "Başlık",
            "description": "Açıklama",
            "url": "Bağlantı",
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ["school", "department", "description", "start_date", "end_date"]
        labels = {
            "school": "Okul",
            "department": "Bölüm",
            "description": "Açıklama",
            "start_date": "Başlangıç Tarihi",
            "end_date": "Bitiş Tarihi",
        }
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "institution", "description", "certificate_url"]
        labels = {
            "name": "Ad",
            "institution": "Kurum",
            "description": "Açıklama",
            "certificate_url": "Sertifika Bağlantısı",
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "level"]
        labels = {
            "name": "Ad",
            "level": "Seviye",
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title","description","date"]
        labels = {
            "title":"Başlık",
            "description":"Açıklama",
            "date":"Tarih",
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "url"]
        labels = {
            "name": "Ad",
            "url": "Bağlantı",
        }





