# Generated by Django 3.2.3 on 2022-03-21 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulado', '0018_resultado_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultado',
            name='simulado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulado.simulado'),
        ),
    ]
