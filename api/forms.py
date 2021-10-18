from django import forms
from api.models import GModel, FModel


class GModelForm(forms.ModelForm):
    class Meta:
        model = GModel
        fields = '__all__'


class FModelForm(forms.ModelForm):
    class Meta:
        model = FModel
        fields = '__all__'
