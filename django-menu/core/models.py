from django.db import models
from uuid import uuid4
from django.urls import reverse
from pytils.translit import slugify
from mptt.models import MPTTModel, TreeForeignKey


def unique_slugify(instance, slug):
    # Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug


class MenuItem(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, editable=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    time_created = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['level']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('menu_item', kwargs={'menu_item_slug': self.slug})

    def save(self, *args, **kwargs):
        # Сохранение полей модели при их отсутствии заполнения
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'