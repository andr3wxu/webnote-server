from django.urls import path
from .views import NoteView, LoginView, SignUpView, TestTokenView

urlpatterns = [
    path('notes/', NoteView.as_view()),  # parent class has method as_view
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('test-token/', TestTokenView.as_view(), name='test-token'),
]
