from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator

class Profile(models.Model):
    ROLE_OWNER = "owner"

    ROLE_CHOICES = [
        (ROLE_OWNER, "Owner"),
    ]

    user = models.OneToOneField( #django'nun built-in User modeli üzerine kurulmuş "Profile" yapısı
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_OWNER,
    )
    biography = models.TextField(
    blank=True,
    )
    phone_number = models.CharField(
    max_length=20,
    blank=True,
    validators=[
        RegexValidator(
            regex=r"^\+?[0-9\s()-]+$",
            message="Geçerli bir telefon numarası giriniz.",
        ),
    ],
    )
    cv = models.FileField(upload_to="cvs/",blank=True,validators=[FileExtensionValidator(allowed_extensions=["pdf"])]) 
    #upload_to="cvs/": yüklenen klasörün medya klasörü altına kaydedileceğini söyler 
    image = models.ImageField(upload_to="pp/",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_owner(self):
        return self.role == self.ROLE_OWNER

# Diğer ekstra modeller (Experience,Project,Education,Course,Skill) built-in olan User modeline bağlıdır !

class Experience(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    company = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField(blank=True)
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
    )

    def __str__(self):
        return self.title


class Education(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="educations",
    )
    school = models.CharField(max_length=150)
    department = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.school} - {self.department}"


class Course(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    name = models.CharField(max_length=150)
    institution = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    certificate_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    LEVEL_BEGINNER = "beginner"
    LEVEL_INTERMEDIATE = "intermediate"
    LEVEL_ADVANCED = "advanced"
    LEVEL_EXPERT = "expert"

    SKILL_CHOICES = [
        (LEVEL_BEGINNER, "Başlangıç"),
        (LEVEL_INTERMEDIATE, "Orta"),
        (LEVEL_ADVANCED, "İleri"),
        (LEVEL_EXPERT, "Uzman"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=SKILL_CHOICES, blank=True)

    def __str__(self):
        return self.name


class Hobby(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hobbies",
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Blog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blogs",
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    image = models.ImageField(
        upload_to="blogs/",
        blank=True,
    )

    def __str__(self):
        return self.title

class Contact(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    name = models.CharField(max_length=100)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name


