# Generated by Django 3.2.3 on 2022-03-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulado', '0013_alter_questao_simulado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questao',
            name='pontuacao',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]