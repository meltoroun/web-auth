from . import views
from django.urls import path
from .views import file_operation

urlpatterns = [
    # path("", views.MyView.as_view()),
    path('encdes/', views.file_operation, name='file_operation'),
    ]

