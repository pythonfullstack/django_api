from django.urls import path
from api.views import upload_gmodel, upload_fmodel, voice_clone

app_name = 'api'

urlpatterns = [
    path('upload-gmodel', upload_gmodel, name='upload_gmodel'),
    path('upload-fmodel', upload_fmodel, name='upload_fmodel'),
    path('cloning', voice_clone, name='cloning'),
]
