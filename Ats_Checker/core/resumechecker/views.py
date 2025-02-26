from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import JobDesriptionSerializer,JobDescription

class JobDescriptionAPI(APIView):
    def get(self, request):
        queryset = JobDescription.objects.all()
        serializer = JobDesriptionSerializer(queryset, many=True)
        return Response({
            'status': 'true',
            'data': serializer.data
        })  