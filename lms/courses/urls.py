from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('upload/', views.upload_course, name='upload'),
    path('notes/', views.note_list, name='note_list'),
    path('download/<int:note_id>/', views.download_note, name='download'),
    path('delete/<int:note_id>/', views.delete_note, name='delete'),
]
