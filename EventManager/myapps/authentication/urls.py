from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from myapps.authentication.views import SignUpApi, EmailLoginApi


urlpatterns = [
    path('register/', SignUpApi.as_view()),
    path('login/', EmailLoginApi.as_view())
]
