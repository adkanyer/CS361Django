# Generated by Django 2.1.3 on 2018-11-15 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactinfo',
            name='first_name',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='last_name',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
