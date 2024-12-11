# Generated by Django 5.0.4 on 2024-07-04 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_eventregistration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('director', models.CharField(max_length=100)),
                ('release_year', models.PositiveIntegerField()),
                ('genre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='event_name',
            field=models.CharField(max_length=60),
        ),
    ]
