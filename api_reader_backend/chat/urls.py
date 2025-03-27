from django.urls import path
from .views import (
    APIDocumentationView,
    APIEndpointView,
    ChatView,
    UserAPIKeyView
)

urlpatterns = [
    # API Documentation endpoints
    path('api-docs/', APIDocumentationView.as_view(), name='api-docs'),
    
    # API Endpoints
    path('api-docs/<uuid:api_doc_id>/endpoints/', APIEndpointView.as_view(), name='api-endpoints'),
    
    # Chat endpoints
    path('chat/', ChatView.as_view(), name='chat'),
    path('chat/<uuid:conversation_id>/', ChatView.as_view(), name='chat-detail'),
    
    # User API Key endpoints
    path('api-keys/', UserAPIKeyView.as_view(), name='api-keys'),
    path('api-keys/<uuid:key_id>/', UserAPIKeyView.as_view(), name='api-key-detail'),
]
