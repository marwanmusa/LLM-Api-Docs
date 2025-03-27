from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    APIDocumentationViewSet,
    APIEndpointViewSet,
    ChatViewSet,
    UserAPIKeyViewSet
)

# Create the main router
router = routers.DefaultRouter()
router.register(r'api-docs', APIDocumentationViewSet, basename='api-docs')
router.register(r'api-keys', UserAPIKeyViewSet, basename='api-keys')
router.register(r'chat', ChatViewSet, basename='chat')

# Create nested router for API endpoints
api_docs_router = routers.NestedDefaultRouter(router, r'api-docs', lookup='api_doc')
api_docs_router.register(r'endpoints', APIEndpointViewSet, basename='api-endpoints')

# The DefaultRouter class includes a default API root view
urlpatterns = [
    path('', include(router.urls)),
    path('', include(api_docs_router.urls)),
]
