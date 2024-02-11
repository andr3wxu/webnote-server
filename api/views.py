from django.shortcuts import render
from rest_framework import generics
from .serializers import NoteSerializer
from .models import Note

# Create your views here.


class NoteView(generics.CreateAPIView):  # inherits
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
