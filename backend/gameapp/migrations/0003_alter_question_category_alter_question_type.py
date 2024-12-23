# Generated by Django 5.1.2 on 2024-12-19 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameapp', '0002_question_action_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.IntegerField(choices=[(1, 'Государство'), (2, 'Развлечения'), (3, 'Недвижимость')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.IntegerField(choices=[(1, 'Развернутый'), (2, 'Варианты')]),
        ),
    ]