from rest_framework import serializers
from .models import JobDescription   


class JobDesriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = '__all__'