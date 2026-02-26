from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Enrollment
from .serializer import EnrollmentSerializer


@api_view(['GET', 'POST'])
def enrollment_list_create(request):
    if request.method == 'GET':
        data = Enrollment.objects.all()
        serializer = EnrollmentSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def enrollment_detail(request, pk):
    try:
        obj = Enrollment.objects.get(id=pk)
    except Enrollment.DoesNotExist:
        return Response({"error": "Not found"})

    if request.method == 'GET':
        serializer = EnrollmentSerializer(obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EnrollmentSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        obj.delete()
        return Response({"message": "Deleted"})