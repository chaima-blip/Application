from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
    
class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id' 
class UserRetrieveByID(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        user_id = self.kwargs['id']
        return User.get_user_by_id(user_id)

class UserRetrieveByEmail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        email = self.kwargs['email']
        return User.get_user_by_email(email)

class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        user_id = self.kwargs['id']
        return User.get_user_by_id(user_id)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_user(
            name=request.data.get('name'),
            password=request.data.get('password'),
            email=request.data.get('email')
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        user_id = self.kwargs['id']
        return User.get_user_by_id(user_id)

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            name = serializer.validated_data.get('name')
            password = serializer.validated_data.get('password')
            user = User.add_user(email=email, name=name, password=password)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def validate_password(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        if check_password(password, user.password):
            return Response({'message': 'Password is valid'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'message': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserRetrieveUpdateDestroyByEmail(APIView):
    def get_object(self, email):
        return get_object_or_404(User, email=email)

    def get(self, request, email):
        user = self.get_object(email)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, email):
        user = self.get_object(email)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, email):
        user = self.get_object(email)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserUpdateByEmail(APIView):
    def get_object(self, email):
        return get_object_or_404(User, email=email)

    def put(self, request, email):
        user = self.get_object(email)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            name = serializer.validated_data.get('name')
            password = serializer.validated_data.get('password')
            
            if email:
                user.email = email
            if name:
                user.name = name
            if password:
                user.password = make_password(password)
            
            user.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserDeleteByEmail(APIView):
    def delete(self, request, email):
        user = get_object_or_404(User, email=email)
        user.delete()
        return Response({"message": f"User with email '{email}' has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)