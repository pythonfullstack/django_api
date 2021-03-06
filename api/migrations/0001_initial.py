# Generated by Django 3.2.8 on 2021-10-18 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_voice', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='models')),
            ],
        ),
        migrations.CreateModel(
            name='GModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_voice', models.CharField(max_length=50)),
                ('g_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VoiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_voice', models.CharField(max_length=50)),
                ('model_path', models.FilePathField(max_length=1024)),
            ],
        ),
    ]
