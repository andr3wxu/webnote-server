from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer
from .models import Note

# Create your views here.


class NoteView(generics.CreateAPIView):  # inherits
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class BaseUserView(APIView):
    def post(self, request):
        return Response({})


class LoginView(APIView):
    def post(self, request):
        return Response({})


class SignUpView(APIView):
    def post(self, request):
        return Response({})


class TestTokenView(APIView):
    def post(self, request):
        return Response({})
