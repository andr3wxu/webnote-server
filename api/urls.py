from django.urls import path
from .views import NotesView, NoteView, URLView, LoginView, SignUpView, TestTokenView, LogoutView

urlpatterns = [
    # path('note/', NoteView.as_view()),  # parent class has method as_view
    path('notes/<int:user_id>/', NotesView.as_view(), name='notes'),
    path('note/<int:note_id>/', NoteView.as_view(), name='note'),
    path('url/', URLView.as_view(), name='url'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('test-token/', TestTokenView.as_view(), name='test-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
