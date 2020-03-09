# Generated by Django 2.2.4 on 2020-03-06 02:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_name', models.CharField(max_length=100)),
                ('a_description', models.TextField()),
                ('assignment_points', models.IntegerField()),
                ('assignment_file_path', models.CharField(max_length=100)),
                ('course_id', models.IntegerField()),
                ('due_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('release_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
