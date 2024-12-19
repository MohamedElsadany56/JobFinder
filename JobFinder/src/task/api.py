from .models import Task
from .serializers import JobSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics


@api_view(['GET'])
def job_list_api(request):
    all_jobs = Task.objects.all()
    data = JobSerializer(all_jobs, many=True).data
    return Response({'data':data})
