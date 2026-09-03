from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_ADMIN  = "admin"
    ROLE_USER   = "user"
    ROLE_OWNER = "owner"
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_USER,  "User"),
        (ROLE_OWNER,  "Owner"),
    ]

    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)
    created_at = models.DateTimeField(auto_now_add=True)
    chat_title_fallback_seq = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

