from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import JobDesriptionSerializer,JobDescription,ResumeSerializer,Resume
from .analyzer import process_resume,process_job_description
from scripts import process_candidate,calculate_skill_score,calculate_project_relevance,fuzzy_candidate_Scoring

class JobDescriptionAPI(APIView):
    def get(self, request):
        queryset = JobDescription.objects.all()
        serializer = JobDesriptionSerializer(queryset, many=True)
        return Response({
            'status': 'true',
            'data': serializer.data
        })  
    


class AnalyzeResumeAPI(APIView) :
    def post(self,request) :
        print("start")
        try :
            data = request.data
            if not data.get('job_description') :
                return Response({
                    'status' : False,
                    'message':'job_description is required',
                    'data' :{}
                })
            serializer = ResumeSerializer(data=data)
            if not serializer.is_valid() :
                return Response({
                        'status' : False,
                        'message':'error',
                        'data' :serializer.errors
                    })
            
            serializer.save()
            _data = serializer.data
            job_id = data.get("job_description")
            resume_instance = Resume.objects.get(id=_data['id'])
            resume_path = resume_instance.resume.path
            data = process_resume(resume_path,JobDescription.objects.get(id=job_id).job_description)
            job_data = process_job_description(JobDescription.objects.get(id=job_id).job_description)
            
            job = JobDescription.objects.filter(id=job_id).first()
            print("start")
            rank = process_candidate(dict(data),str(job),dict(job_data.get("skills")),calculate_skill_score,calculate_project_relevance,fuzzy_candidate_Scoring)
            print("exit")
            print(rank)
            data["rank"] = rank

            return Response({
                'status' : True,
                'message': str(job),
                'data' : data,
                'job_data':job_data
            })
        
        except Exception as e:  
            return Response({
                'status' : False,
                'message': str(e),
                'data' :{}
            })
        

