from django.db import models
import gdown
from django.conf import settings
import os


# Create your models here.

class VoiceModel(models.Model):
    name_of_voice = models.CharField(max_length=50)
    model_path = models.CharField(max_length=1024)

    @staticmethod
    def check_exist(name):
        return VoiceModel.objects.filter(name_of_voice=name)

    @staticmethod
    def create_model(name, model_path):
        VoiceModel.objects.create(name_of_voice=name, model_path=model_path)

    def __str__(self):
        return self.name_of_voice


class GModel(models.Model):
    name_of_voice = models.CharField(max_length=50, unique=True)
    g_id = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        d = 'https://drive.google.com/uc?id='
        if self.name_of_voice in GModel.objects.all().values('name_of_voice'):
            return
        if VoiceModel.check_exist(name=self.name_of_voice):
            return
        model_path = os.path.join(settings.MEDIA_ROOT, 'models', self.name_of_voice)
        gdown.download(d + self.g_id, model_path, quiet=False)
        VoiceModel.create_model(name=self.name_of_voice, model_path=model_path)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_of_voice


class FModel(models.Model):
    name_of_voice = models.CharField(max_length=50)
    file = models.FileField(upload_to='models')

    def save(self, *args, **kwargs):
        if VoiceModel.check_exist(name=self.name_of_voice):
            return
        VoiceModel.create_model(name=self.name_of_voice, model_path=self.file.path)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_of_voice
