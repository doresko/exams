# Generated by Django 2.2.6 on 2019-10-25 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0011_auto_20191025_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
