# Generated by Django 5.1.6 on 2025-03-22 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes_app', '0002_alter_tag_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
