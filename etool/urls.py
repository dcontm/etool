from django.urls import path
from . import views

urlpatterns = [
    path('', views.EntryPointView.as_view(), name='entrypoint')
]
