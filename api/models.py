from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя компании')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание'
                                   )

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Описание')
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Компания'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-id',)

    def __str__(self):
        return self.title
