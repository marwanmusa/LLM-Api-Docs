from django.contrib import admin
from .models import APIDocumentation, APIEndpoint, Conversation, Message, VectorCache, UserAPIKey

@admin.register(APIDocumentation)
class APIDocumentationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(APIEndpoint)
class APIEndpointAdmin(admin.ModelAdmin):
    list_display = ('url', 'http_method', 'api_doc', 'created_at')
    list_filter = ('http_method', 'api_doc')
    search_fields = ('url', 'description')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('topic', 'user', 'api_doc', 'endpoint', 'created_at')
    list_filter = ('api_doc', 'user')
    search_fields = ('topic',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'is_user', 'created_at')
    list_filter = ('is_user', 'conversation')
    search_fields = ('content',)

@admin.register(VectorCache)
class VectorCacheAdmin(admin.ModelAdmin):
    list_display = ('api_doc', 'created_at', 'updated_at')
    list_filter = ('api_doc',)

@admin.register(UserAPIKey)
class UserAPIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('user__username',)
