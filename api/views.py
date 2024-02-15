from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import NoteSerializer, UserSerializer
from .models import Note
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404


class NotesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    # ENDPOINT: retrieves all notes from the database corresponding to specified user_id URL param.
    def get(self, request, user_id):
        try:
            queryset = Note.objects.filter(
                user=user_id).order_by('-date_created')
            # queryset: list of model instances
            # many=True handles list of items
            serialized = NoteSerializer(queryset, many=True)
            # don't need is_valid() here since model is already part of database, and therefore, implicitly valid
            return Response(serialized.data)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ENDPOINT: inserts new Note instance into the database
    def post(self, request, user_id):
        data = request.data
        serialized = NoteSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    # ENDPOINT: retrives specific note by note_id
    def patch(self, request, note_id):
        try:
            print(request.data)
            note = Note.objects.get(id=note_id)
            serializer = NoteSerializer(note, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist:
            return Response({"message": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, note_id):
        try:
            note = Note.objects.get(id=note_id)
            serialized = NoteSerializer(note)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Note.DoesNotExist:
            return Response({"message": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class URLView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication, SessionAuthentication]

    # ENDPOINT: retrives specific note by URL
    def post(self, request):
        try:
            note = Note.objects.filter(
                url=request.data["url"]).order_by('-date_created')[0]
            serialized = NoteSerializer(note)
            if request.data["user_id"] == str(serialized.data["user"]):
                return Response(serialized.data, status=status.HTTP_200_OK)
            return Response({"message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({"message": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):

    # ENDPOINT: handles login request
    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        print(token)
        serializer = UserSerializer(instance=user)

        response = Response(
            {"token": token.key, "username": serializer.data["username"], "id": serializer.data["id"]})
        response.set_cookie(key="wn_auth_token", value=token.key)
        return response


class TestTokenView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    # ENDPOINTS: verifies that user is authenticated
    def get(self, request):
        return Response({"isAuthenticated": True, "user": request.user.username})


class SignUpView(APIView):

    # ENDPOINT: handles sign up request
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            # django handles password hashing
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            response = Response(
                {"token": token.key, "username": serializer.data["username"], "id": serializer.data["id"]})
            response.set_cookie(key="wn_auth_token", value=token.key)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # ENDPOINT: logs user out
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully.'})
