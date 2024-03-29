# Generated by Django 2.2.6 on 2019-10-14 22:05

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0005_auto_20190919_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='level',
            name='description',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='description',
        ),
        migrations.AlterField(
            model_name='citation',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='exams.Problem'),
        ),
        migrations.DeleteModel(
            name='Year',
        ),
    ]
