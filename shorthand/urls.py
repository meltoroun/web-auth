from django.urls import path
from .views import decode_end_of_line, encode_end_of_line

urlpatterns = [
    path('encode/', encode_end_of_line, name='encode'),
    path('decode/', decode_end_of_line, name='decode')

]