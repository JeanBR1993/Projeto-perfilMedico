# Generated by Django 5.1.3 on 2025-05-14 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_registrovacinacao_delete_vacinas'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fichacadastral',
            options={'verbose_name': 'Ficha cadastral', 'verbose_name_plural': 'Fichas cadastrais'},
        ),
        migrations.RemoveField(
            model_name='medicamentoreceitado',
            name='dosagem',
        ),
    ]
