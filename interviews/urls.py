from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet, InterviewViewSet

router = DefaultRouter()
router.register(r'candidates', CandidateViewSet)
router.register(r'interviews', InterviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
