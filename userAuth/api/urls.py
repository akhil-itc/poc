from django.urls import path
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import UserViewSet


router = DefaultRouter()

router.register(r'', UserViewSet)
snippet_highlight = UserViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

urlpatterns = router.urls+format_suffix_patterns([

    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),

])
