import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from api.forms import GModelForm, FModelForm
from api.models import VoiceModel
from api.cloning.inference import inference


# Create your views here.


@csrf_exempt
def upload_gmodel(request):
    if request.method == 'POST':
        form = GModelForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse({
                "Result": "Failed",
                "Error": "Fields doesn't valid"
            }, status=204)


@csrf_exempt
def upload_fmodel(request):
    if request.method == 'POST':
        form = FModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({
                "Result": "Success",
                "Message": "Model has been uploaded Successfully."
            }, status=201)
        else:
            return JsonResponse({
                "Result": "Failed",
                "Message": "Fields doesn't valid"
            }, status=204)


def voice_clone(request):
    if request.method == "GET":
        data = json.loads(request.body)
        name = data["name"]
        text = data["text"]
        model = get_object_or_404(VoiceModel, name_of_voice=name)
        model_path = model.model_path
        inference(text=text, model_path=model_path)
        return JsonResponse({
            "Result": "Success",
            "Message": text
        }, status=200)
