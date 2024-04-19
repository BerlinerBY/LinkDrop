# Generated by Django 5.0.4 on 2024-04-18 15:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_storage', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=350)),
                ('url_field', models.URLField(max_length=300)),
                ('url_to_image', models.URLField(max_length=300)),
                ('type_of_link', models.CharField(default='website', max_length=20)),
                ('date_of_created', models.DateTimeField(auto_now_add=True)),
                ('date_of_changed', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='link_storage.collection')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
                'ordering': ('date_of_created',),
            },
        ),
    ]
