from django.contrib.auth import get_user_model
from django.db import models

from api.models import Company

User = get_user_model()


class Roles(models.TextChoices):
    """Роли пользователей."""
    MODERATOR = 'moderator'
    USER = 'user'


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        related_name='profiles',
        verbose_name='Компания',
        null=True,
        blank=True,
    )

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.user.username
