from rest_framework import serializers
from .models import APIDocumentation, APIEndpoint, Conversation, Message, VectorCache, UserAPIKey

class APIDocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIDocumentation
        fields = ['id', 'name', 'description', 'documentation_json', 'created_at', 'updated_at', 'user']
        read_only_fields = ['id', 'created_at', 'updated_at']

class APIEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIEndpoint
        fields = ['id', 'api_doc', 'url', 'http_method', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'content', 'is_user', 'created_at']
        read_only_fields = ['id', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'topic', 'api_doc', 'endpoint', 'created_at', 'updated_at', 'user', 'messages']
        read_only_fields = ['id', 'created_at', 'updated_at']

class VectorCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorCache
        fields = ['id', 'api_doc', 'content', 'vector', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserAPIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAPIKey
        fields = ['id', 'user', 'openai_api_key', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'openai_api_key': {'write_only': True}
        }
