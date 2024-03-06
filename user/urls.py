from django.urls import path, include

from user.apiviews import CreateUserView
from user.apps import UserConfig

app_name = UserConfig.name

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
]
