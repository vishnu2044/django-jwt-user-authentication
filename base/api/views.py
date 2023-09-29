from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from .serializers import NotSerializer, UserRegister, ProfileSerializer, SingleProfileSerializer
from base.models import Note, UserProfile
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.filters import SearchFilter




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class Register(APIView):
    def post(self, request, format=None):
        serializer = UserRegister(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'response': 'registered',
                'username': user.username,
                'email': user.email,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    print('===============>>', user)


    if user.is_superuser:
        data = {
            "superuser": True,
            'response': 'registered',
            'username': user.username,
            'email': user.email
        }
    else:
        profile = UserProfile.objects.get(user_id=user)
        
        serializer = ProfileSerializer(profile)
        data = serializer.data
        data = {
            'response': 'registered',
            'username': user.username,
            'email': user.email,
            'phone_no': profile.Phone_no,
            'dob': profile.date_of_birth,
            # 'profile_img': profile.profile_img
        }
    return Response(data)


@api_view(["GET"])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(routes)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getNotes(request):
    user = request.user
    notes = Note.objects.filter(user=user)
    serializer = NotSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateProfile(request):

    user = request.user
    profile = UserProfile.objects.get(user_id = user)
    
    if 'profile_imge' in request.FILES:
        profile.profile_img = request.FILES['profile_img']
    serializer = ProfileSerializer(instance = profile, data = request.data, partial = True)
    print(serializer, "##########################################################")
    if serializer.is_valid():
        serializer.save()
        print("updateddd!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        data = serializer.data
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        user.save()
        data['response'] = 'registered'
        data['username'] = user.username
        data['email'] = user.email
    else:
        data = serializer.errors
        print("Errors!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", data)
    return Response(data)


class UserList(ListCreateAPIView):
    queryset = User.objects.all().exclude(is_superuser = True)
    serializer_class = UserRegister
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username']



class UserDetails(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegister
    lookup_field = 'id'

    


class GetSingleUser(RetrieveAPIView):
    serializer_class = SingleProfileSerializer

    def get_object(self):
        user_id = self.kwargs.get('id')
        return UserProfile.objects.get(user_id = user_id)
 