from django.db import models
from django.utils.text import slugify
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Collection(models.Model):
    title = models.CharField(max_length=75, blank=False, unique=True)
    description = models.CharField(max_length=350, blank=True, default="")
    date_of_created = models.DateTimeField(auto_now_add=True)
    date_of_changed = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='collections'
        )
    
    class Meta:
        verbose_name = 'collection'
        verbose_name_plural = 'collections'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Link(models.Model):
    title = models.CharField(max_length=100, blank=False, default="")
    description = models.CharField(max_length=350, blank=True, default="")
    url_field = models.URLField(max_length=300, blank=False)
    url_to_image = models.URLField(max_length=300, blank=False)
    type_of_link = models.CharField(max_length=20, blank=False, default="website")
    date_of_created = models.DateTimeField(auto_now_add=True)
    date_of_changed = models.DateTimeField(auto_now=True)
    
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    collection = models.ForeignKey(
            Collection, 
            on_delete=models.CASCADE,
            related_name='links'
        )
    created_by = models.ForeignKey(
            User, 
            on_delete=models.CASCADE, 
            related_name='links'
        )
    
    class Meta:
        ordering = ('date_of_created',)
        verbose_name = 'link'
        verbose_name_plural = 'links'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Link, self).save(*args, **kwargs)

    def __str__(self):
        return self.title