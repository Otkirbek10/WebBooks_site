# Generated by Django 5.0.2 on 2024-02-21 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name="Author's name")),
                ('slug', models.SlugField(max_length=200, null=True, unique=True)),
                ('picture', models.ImageField(null=True, upload_to='authors/', verbose_name="Author's photo")),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='Date of death')),
                ('biography', models.TextField(null=True, verbose_name='Biography of an author')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Genre books')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Language')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Copy status of a book')),
            ],
            options={
                'verbose_name_plural': 'Statuses',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title of a book')),
                ('book_slug', models.SlugField(max_length=200, null=True, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='book_images/', verbose_name='Photo of a book')),
                ('description', models.TextField(max_length=1500, verbose_name='About a book')),
                ('isbn', models.CharField(max_length=13, verbose_name='ISBN of a book')),
                ('author', models.ManyToManyField(to='catalog.author', verbose_name='Authors of a book')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.genre', verbose_name='Genre of a book')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.language', verbose_name='language of a book')),
            ],
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inv_nom', models.CharField(max_length=20, null=True, verbose_name='Inventory number')),
                ('imprint', models.CharField(max_length=200, verbose_name='Publishing house')),
                ('due_back', models.DateField(blank=True, null=True, verbose_name='Staus expire date')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.status', verbose_name='Book copy status')),
            ],
        ),
    ]
