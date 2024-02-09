from django.urls import path
from .views import NoteView

urlpatterns = [
    path('notes', NoteView.as_view()) # parent class has method as_view
]