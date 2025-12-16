from django.urls import path
from .views import ChatView, HandoffView

urlpatterns = [
    path("chat/", ChatView.as_view()),
    path("handoff/", HandoffView.as_view()),
]
