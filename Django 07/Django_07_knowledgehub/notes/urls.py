from django.urls import path

from . import views

urlpatterns = [
    path("", views.notes_list, name="notes_list"),
    path("create/", views.note_create, name="note_create"),
    path("edit/<int:note_id>", views.note_edit, name="note_edit"),
    path("delete/<int:note_id>", views.note_delete, name="note_delete"),
    path("<int:note_id>", views.note_detail, name="note_detail"),

]