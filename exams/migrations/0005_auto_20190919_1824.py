# Generated by Django 2.2.5 on 2019-09-19 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0004_auto_20190918_1944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='country',
        ),
        migrations.AlterField(
            model_name='citation',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='exams.Place'),
        ),
        migrations.AlterField(
            model_name='citation',
            name='year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='exams.Year'),
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]
