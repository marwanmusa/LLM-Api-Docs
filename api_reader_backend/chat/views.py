from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import APIDocumentation, APIEndpoint, Conversation, Message, VectorCache, UserAPIKey
from .serializers import (
    APIDocumentationSerializer, APIEndpointSerializer,
    ConversationSerializer, MessageSerializer, VectorCacheSerializer,
    UserAPIKeySerializer
)
from .utils import (
    cache_api_response, cache_vector_data, get_cached_vector,
    cache_conversation_history, get_cached_conversation,
    clear_conversation_cache, invalidate_api_cache
)
import openai
from django.conf import settings
import json

class APIDocumentationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = APIDocumentationSerializer

    def get_queryset(self):
        return APIDocumentation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        invalidate_api_cache('api_docs')

    def perform_update(self, serializer):
        serializer.save()
        invalidate_api_cache('api_docs')

    def perform_destroy(self, instance):
        instance.delete()
        invalidate_api_cache('api_docs')

class APIEndpointViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = APIEndpointSerializer

    def get_queryset(self):
        api_doc_id = self.kwargs.get('api_doc_id')
        return APIEndpoint.objects.filter(api_doc_id=api_doc_id)

    def perform_create(self, serializer):
        api_doc = get_object_or_404(APIDocumentation, id=self.kwargs.get('api_doc_id'), user=self.request.user)
        serializer.save(api_doc=api_doc)
        invalidate_api_cache('api_endpoints')

    def perform_update(self, serializer):
        serializer.save()
        invalidate_api_cache('api_endpoints')

    def perform_destroy(self, instance):
        instance.delete()
        invalidate_api_cache('api_endpoints')

class ChatViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        data = request.data
        conversation_id = data.get('conversation_id')
        message_content = data.get('message')
        endpoint_id = data.get('endpoint_id')

        if not message_content or not endpoint_id:
            return Response(
                {"error": "Message content and endpoint_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        endpoint = get_object_or_404(APIEndpoint, id=endpoint_id)
        
        # Get or create conversation
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        else:
            conversation = Conversation.objects.create(
                topic=f"Chat about {endpoint.url}",
                api_doc=endpoint.api_doc,
                endpoint=endpoint,
                user=request.user
            )

        # Create user message
        user_message = Message.objects.create(
            conversation=conversation,
            content=message_content,
            is_user=True
        )

        # Get user's API key or use default
        try:
            user_api_key = UserAPIKey.objects.get(user=request.user, is_active=True)
            openai.api_key = user_api_key.openai_api_key
        except UserAPIKey.DoesNotExist:
            openai.api_key = settings.OPENAI_API_KEY

        # Check for cached vector data
        vector_data = get_cached_vector(endpoint.api_doc.id, message_content)
        if not vector_data:
            # Prepare context for the AI
            context = {
                "api_doc": endpoint.api_doc.documentation_json,
                "endpoint": {
                    "url": endpoint.url,
                    "method": endpoint.http_method,
                    "description": endpoint.description
                },
                "conversation_history": [
                    {"role": "user" if msg.is_user else "assistant", "content": msg.content}
                    for msg in conversation.messages.all().order_by('created_at')[-5:]
                ]
            }

            try:
                # Call OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an API documentation assistant. Help users understand and work with APIs."},
                        {"role": "user", "content": json.dumps(context)}
                    ]
                )

                # Cache the vector data
                vector_data = response.choices[0].message.content
                cache_vector_data(endpoint.api_doc.id, message_content, vector_data)

                # Create AI response message
                ai_message = Message.objects.create(
                    conversation=conversation,
                    content=vector_data,
                    is_user=False
                )

                # Clear conversation cache
                clear_conversation_cache(conversation.id)

                return Response({
                    "conversation": ConversationSerializer(conversation).data,
                    "user_message": MessageSerializer(user_message).data,
                    "ai_message": MessageSerializer(ai_message).data
                })

            except Exception as e:
                return Response(
                    {"error": f"Error generating AI response: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            # Use cached vector data
            ai_message = Message.objects.create(
                conversation=conversation,
                content=vector_data,
                is_user=False
            )

            # Clear conversation cache
            clear_conversation_cache(conversation.id)

            return Response({
                "conversation": ConversationSerializer(conversation).data,
                "user_message": MessageSerializer(user_message).data,
                "ai_message": MessageSerializer(ai_message).data
            })

class UserAPIKeyViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserAPIKeySerializer

    def get_queryset(self):
        return UserAPIKey.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        invalidate_api_cache('api_keys')

    def perform_update(self, serializer):
        serializer.save()
        invalidate_api_cache('api_keys')

    def perform_destroy(self, instance):
        instance.delete()
        invalidate_api_cache('api_keys')
