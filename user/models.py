from django.contrib.auth import get_user_model
from django.db import models

from api.models import Company

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Компания'
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.user.username