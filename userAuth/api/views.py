from django.contrib.auth.models import User
from rest_framework import viewsets, renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializers


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializers

    queryset = User.objects.all()

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet )

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)