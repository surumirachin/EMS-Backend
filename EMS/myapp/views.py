from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from myapp.models import Leave
from myapp.serializers import LeaveSerializer
from myapp.serializers import AuthTokenSerializer
from myapp.serializers import EmployeeSerializer, UserSerializer
# from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from myapp.models import User
from django.core.files.storage import default_storage
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser

# Create your views here.


class profileView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data, context={'request': request})
       
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username':user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_id': user.pk,
            'email': user.email,
            'admin':user.is_superuser,
        })

     

@api_view(["GET", "POST", "PUT", "DELETE", "PATCH"])

# @csrf_exempt

def employeeApi(request, **kwargs):
    id = kwargs.get("id", None)
    if request.method=='GET':
        if id:
            employee = User.objects.get(id=id)
            employees_serializer = EmployeeSerializer(employee)
        else:
            employees = User.objects.filter(is_superuser=False)
            employees_serializer = EmployeeSerializer(employees, many=True)
        return JsonResponse(employees_serializer.data,  safe=False)

    elif request.method=='POST':
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Employee Added Successfully!!" ,  safe=False)
        
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method=='PUT':
        employee_data = JSONParser().parse(request)
        employee=User.objects.get(id=kwargs.get("id"))
        serializer=UserSerializer(employee, data=employee_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
       
        return JsonResponse("Failed to Update.",   safe=False)

    elif request.method=='DELETE':
        employee=User.objects.get(id=kwargs.get("id"))
        employee.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)

    elif request.method=='PATCH':
        employee=User.objects.get(id=kwargs.get("id"))
        employee.patch()
        return JsonResponse("updated Succeffully!!", safe=False)


@csrf_exempt
def SaveFile(request ):
    file=request.FILES.get('media')
    file_name = default_storage.save(file.name,file)
    return JsonResponse(file_name,safe=False)

@api_view(["GET", "POST", "PUT", "DELETE"])


@csrf_exempt
def leaveApi(request,id=0):
    if request.method=='GET':
        employees = Leave.objects.all()
        employees_serializer = LeaveSerializer(employees, many=True)
        return JsonResponse(employees_serializer.data, safe=False)

    elif request.method=='POST':
        serializer = LeaveSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse("Leave Approved!!" , safe=False)
    return JsonResponse(serializer.errors, status=400)







