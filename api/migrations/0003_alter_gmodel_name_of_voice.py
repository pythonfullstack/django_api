# Generated by Django 3.2.8 on 2021-10-18 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_voicemodel_model_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gmodel',
            name='name_of_voice',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
