from rest_framework import serializers
from .models import Sponsor, Student, Metsenat


class SponsorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


class SponsorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['organization', 'full_name', 'phone_number', 'payment_amount', 'company_name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        depth = 1


class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['full_name', 'phone_number', 'otm', 'student_type', 'contract_amount']


class MetsenatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metsenat
        fields = ['student', 'payment', 'sponsor']
