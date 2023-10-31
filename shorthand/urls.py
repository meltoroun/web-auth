from django.urls import path
from .views import encode_text

urlpatterns = [
    path('encode/', encode_text, name='encode_text'),
]