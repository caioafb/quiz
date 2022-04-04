# Generated by Django 3.2.10 on 2022-04-04 23:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, unique=True)),
                ('pub_date', models.DateTimeField(verbose_name='Pub Date')),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('pub_date', models.DateTimeField(verbose_name='Pub Date')),
            ],
        ),
        migrations.CreateModel(
            name='Userr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.FloatField()),
                ('pub_date', models.DateTimeField(verbose_name='Pub Date')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz')),
                ('userr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.userr')),
            ],
        ),
        migrations.AddField(
            model_name='quiz',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.userr'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='question',
            field=models.ManyToManyField(blank=True, null=True, related_name='quiz', to='quiz.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.userr'),
        ),
        migrations.AddField(
            model_name='question',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.label'),
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
            ],
        ),
    ]