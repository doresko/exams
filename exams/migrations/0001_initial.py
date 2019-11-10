# Generated by Django 2.2.5 on 2019-09-14 17:17

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Citation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=256)),
                ('url', models.TextField(blank=True, max_length=256, null=True)),
                ('other', models.TextField(blank=True, max_length=1024, null=True)),
                ('authors', models.ManyToManyField(help_text='Szerzők', to='exams.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Coutries',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=64, unique=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PythonLibrary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(max_length=1024)),
                ('url', models.TextField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Python libraries',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('short_description', models.TextField()),
                ('full_description', models.TextField()),
                ('solution_code', models.TextField()),
                ('solution_explanation', models.TextField()),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('levels', models.ManyToManyField(help_text='Milyen tudásszintű hallgatóknak ajánljuk a feladatot', to='exams.Level')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='exams.Problem')),
                ('recommended_libraries', models.ManyToManyField(blank=True, help_text='A feladat megoldásához javasolt programkönyvtárak.', to='exams.PythonLibrary')),
                ('skills', models.ManyToManyField(help_text='Készségek, melyeket a feladat fejleszt. ', to='exams.Skill')),
                ('sources', models.ManyToManyField(to='exams.Citation')),
                ('tags', models.ManyToManyField(help_text='Általános tag-ek, amelyekkel keresni lehet, pl. téma, jelleg, stb.', to='exams.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exams.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Hint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.PositiveSmallIntegerField(help_text='Sorszám: hányadikként jelenjen meg a segítség')),
                ('hint', models.CharField(max_length=256)),
                ('explanation', models.TextField(blank=True, null=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Problem')),
            ],
        ),
        migrations.AddField(
            model_name='citation',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='exams.Place'),
        ),
        migrations.AddField(
            model_name='citation',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='exams.Publisher'),
        ),
        migrations.AddField(
            model_name='citation',
            name='year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='exams.Year'),
        ),
    ]