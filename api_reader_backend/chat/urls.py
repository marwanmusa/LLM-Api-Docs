from django.urls import path
from .views import ChatHistoryView, ClearChatHistoryView

urlpatterns = [
    path('chat-history/', ChatHistoryView.as_view(), name='chat-history'),
    path('chat-history/<uuid:pk>/', ChatHistoryView.as_view(), name='chat-history-detail'),
    path('clear-history/', ClearChatHistoryView.as_view(), name='clear-history'),
]
