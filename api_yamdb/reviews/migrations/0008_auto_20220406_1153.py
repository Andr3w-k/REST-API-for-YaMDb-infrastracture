# Generated by Django 2.2.16 on 2022-04-06 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20220404_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genres',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название жанра'),
        ),
        migrations.AlterField(
            model_name='genres',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug жанра'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='genres', to='reviews.Genres'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(verbose_name='Год релиза'),
        ),
    ]