from . import views
from django.urls import path
from .views import encrypt_file, decrypt_file

urlpatterns = [
    # path("", views.MyView.as_view()),
    path('encrypt/', encrypt_file, name='encrypt_file'),
    path('decrypt/', decrypt_file, name='decrypt_file'),
    ]
