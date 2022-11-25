from rest_framework.response import Response
from .serializers import (SponsorListSerializer,
                          SponsorCreateSerializer,
                          StudentSerializer,
                          StudentCreateSerializer,
                          MetsenatCreateSerializer,
                          )
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from .models import Sponsor, Student, Metsenat
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from .paginator import ResultsSetPagination

Months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']


class DashboardViews(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_amount = 0
        total_request = 0
        money_due = 0
        metsenats = Metsenat.objects.all()
        serializer = MetsenatCreateSerializer(metsenats, many=True)
        for metsen in metsenats:
            total_amount += metsen.payment
            total_request += metsen.student.contract_amount
            money_due += metsen.student.contract_amount - metsen.student.allocated_amount
        statistika = []
        students = Student.objects.all()
        sponsors = Sponsor.objects.all()
        for month in Months:
            student_count = 0
            sponsor_count = 0
            for student in students:
                if int(month) == student.add_day.month:
                    student_count += 1
            for sponsor in sponsors:
                if int(month) == sponsor.add_day.month:
                    sponsor_count += 1
            statis = {'month': month, 'student': student_count, 'sponsor': sponsor_count}
            statistika.append(statis)
        return Response({'metsenat': serializer.data, 'total_amount': total_amount, 'total_request': total_request, 'money_due': money_due, 'statistika': statistika})


class SponsorCreateViews(CreateAPIView):
    serializer_class = SponsorCreateSerializer


class SponsorListViews(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Sponsor.objects.all()
    serializer_class = SponsorListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'payment_amount', 'add_day']
    pagination_class = ResultsSetPagination


class SponsorDetailViews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def put(self, request, pk):
        sponsor = Sponsor.objects.get(pk=pk)
        serializer = SponsorListSerializer(sponsor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        sponsor = Sponsor.objects.get(pk=pk)
        sponsor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentListViews(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student_type', 'otm']
    pagination_class = ResultsSetPagination


class StudentCreateViews(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer


class StudentViews(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        student = Student.objects.get(pk=pk)
        serializer_student = StudentSerializer(student, many=False)
        mentanet = Metsenat.objects.filter(student=student)

        response = []
        for key in mentanet:
            sponsor = {}
            sponsor['id'] = key.sponsor.id
            sponsor['full_name'] = key.sponsor.full_name
            sponsor['payment'] = key.payment
            response.append(sponsor)
        return Response({'student': serializer_student.data, 'metsenat': response})


class MentanetViews(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        metsenats = Metsenat.objects.all()
        serializer = MetsenatCreateSerializer(metsenats, many=True)
        return Response(serializer.data)

    def post(self, request):
        student = Student.objects.get(pk=request.data['student'])
        payment = request.data['payment']
        sponsor = Sponsor.objects.get(pk=request.data['sponsor'])
        serializer = MetsenatCreateSerializer(data=request.data)
        if student.rest_money() >= payment:
            if sponsor.rest_money() >= payment:
                if serializer.is_valid():
                    student.allocated_amount = student.allocated_amount + payment
                    sponsor.allocated_amount = sponsor.allocated_amount + payment
                    student.save()
                    sponsor.save()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': f"Homiyni mablag'i yetmaydi. Homiyda {sponsor.rest_money()} so'm qolgan."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": f"Talabaga yetarli pul yig'ilgan yoki {payment} dan kam pul kerak."},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


