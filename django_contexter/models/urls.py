from django.urls import path

from django_contexter.models import views

urlpatterns = [path("", views.Index.as_view())]
