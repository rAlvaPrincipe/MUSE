from django.urls import path
from . import views

urlpatterns = [
    path("lineage", views.lineage_artist, name="lineage_artist")
]