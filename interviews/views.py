from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

from .models import Candidate, Interview
from .serializers import CandidateSerializer, InterviewSerializer

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class InterviewPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

class InterviewViewSet(viewsets.ModelViewSet):
    pagination_class = InterviewPagination #пагинация
    queryset = Interview.objects.all().order_by('-date')
    serializer_class = InterviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status'] #фильтрация по статусу
    search_fields = ['candidate__name'] #поиск по имени

    @action(methods=['GET'], detail=False, url_path='search-mixed')
    def search_mixed(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response([])

        queryset = self.get_queryset().filter(
            Q(candidate__name__icontains=query) | Q(status__icontains=query)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
