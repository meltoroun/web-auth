from django.urls import path
from . import views
from index.views import registration

urlpatterns = [
    # post views
    path("", views.user_login, name="login"),
    path('user/registration/', registration)
]