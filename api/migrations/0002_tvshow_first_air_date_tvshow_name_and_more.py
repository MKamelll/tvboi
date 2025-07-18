# Generated by Django 5.2.2 on 2025-06-13 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tvshow',
            name='first_air_date',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='origin_country',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='original_language',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='overview',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='poster_path',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='vote_average',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='tvshow',
            name='id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]
