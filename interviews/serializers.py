from rest_framework import serializers
from .models import Candidate, Interview

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class InterviewSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)
    candidate_id = serializers.PrimaryKeyRelatedField(
        queryset=Candidate.objects.all(),
        source='candidate',
        write_only=True
    )

    class Meta:
        model = Interview
        fields = ['id', 'candidate', 'candidate_id', 'date', 'status', 'notes', 'created_at']
