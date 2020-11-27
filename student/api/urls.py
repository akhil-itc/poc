
from rest_framework.routers import DefaultRouter

from student.api.views import CourseViewSet

router = DefaultRouter()

router.register(r'course', CourseViewSet)
