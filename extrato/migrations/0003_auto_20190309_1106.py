# Generated by Django 2.1.7 on 2019-03-09 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extrato', '0002_transacao_sinal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transacao',
            options={'ordering': ['-data', 'corretora', 'titulo'], 'verbose_name_plural': 'Transações'},
        ),
    ]
