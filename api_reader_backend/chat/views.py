from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes
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

class APIDocumentationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @cache_api_response('api_docs')
    def get(self, request):
        """Retrieve all API documentation for the current user."""
        docs = APIDocumentation.objects.filter(user=request.user)
        serializer = APIDocumentationSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create new API documentation."""
        serializer = APIDocumentationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # Invalidate cache after creating new documentation
            invalidate_api_cache('api_docs')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APIEndpointView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @cache_api_response('api_endpoints')
    def get(self, request, api_doc_id):
        """Retrieve all endpoints for a specific API documentation."""
        endpoints = APIEndpoint.objects.filter(api_doc_id=api_doc_id)
        serializer = APIEndpointSerializer(endpoints, many=True)
        return Response(serializer.data)

    def post(self, request, api_doc_id):
        """Create a new endpoint for an API documentation."""
        api_doc = get_object_or_404(APIDocumentation, id=api_doc_id, user=request.user)
        serializer = APIEndpointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(api_doc=api_doc)
            # Invalidate cache after creating new endpoint
            invalidate_api_cache('api_endpoints')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @cache_api_response('conversations')
    def get(self, request, conversation_id=None):
        """Retrieve conversation history."""
        if conversation_id:
            # Try to get from cache first
            cached_conversation = get_cached_conversation(conversation_id)
            if cached_conversation:
                return Response(cached_conversation)
            
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
            serializer = ConversationSerializer(conversation)
            response_data = serializer.data
            
            # Cache the conversation
            cache_conversation_history(conversation_id, response_data)
            return Response(response_data)
        else:
            conversations = Conversation.objects.filter(user=request.user)
            serializer = ConversationSerializer(conversations, many=True)
            return Response(serializer.data)

    def post(self, request):
        """Create a new message in a conversation."""
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

class UserAPIKeyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @cache_api_response('api_keys')
    def get(self, request):
        """Retrieve user's API keys."""
        api_keys = UserAPIKey.objects.filter(user=request.user)
        serializer = UserAPIKeySerializer(api_keys, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Add a new API key."""
        serializer = UserAPIKeySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # Invalidate cache after adding new API key
            invalidate_api_cache('api_keys')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, key_id):
        """Delete an API key."""
        api_key = get_object_or_404(UserAPIKey, id=key_id, user=request.user)
        api_key.delete()
        # Invalidate cache after deleting API key
        invalidate_api_cache('api_keys')
        return Response(status=status.HTTP_204_NO_CONTENT)
