from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from .serializers import CourseSerializers
from ..models import Course


# class CourseStudentViewSet(viewsets.ViewSet):
#     serializer_class = CourseSerializers
#     queryset = Course.objects.all()
class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()