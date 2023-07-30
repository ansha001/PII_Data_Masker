from django.contrib import admin
from django.urls import path
from deidentification import views

urlpatterns = [
    path("", views.index, name="index"),
    path("detect/", views.detect, name="detect"),
    path("free-text/", views.free_text, name="free-text"),
    path("table/", views.table, name="table"),
    path("document/", views.document, name="document"),
    path("image/", views.image, name="image"),
    path('textinput/', views.textinput, name='textinput'),
    path('fileinput/', views.fileinput, name='fileinput'),
]
