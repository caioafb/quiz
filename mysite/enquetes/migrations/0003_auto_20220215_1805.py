# Generated by Django 3.2.3 on 2022-02-15 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquetes', '0002_auto_20220215_1746'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autor',
            options={'verbose_name_plural': 'Autores'},
        ),
        migrations.RemoveField(
            model_name='rotulo',
            name='perguntas',
        ),
        migrations.AddField(
            model_name='pergunta',
            name='rotulos',
            field=models.ManyToManyField(to='enquetes.Rotulo'),
        ),
    ]
