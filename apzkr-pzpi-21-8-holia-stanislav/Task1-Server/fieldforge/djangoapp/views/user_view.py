from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView # type: ignore 
from ..renderers import UserJSONRenderer
from ..models import Training, User
from rest_framework.generics import RetrieveAPIView # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from ..serializers import (
 PublicUserSerializer, UserSerializer, TrainingSerializer
)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PublicUserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    renderer_classes = (UserJSONRenderer,)
    serializer_class = PublicUserSerializer
    lookup_field = 'uuid'  
    permission_classes = [IsAuthenticated]  


class DeactivateUserView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request):
        user = request.user
        User.objects.deactivate(user.uuid)
        return Response({'status': 'User deactivated'}, status=status.HTTP_200_OK)
    
class UserTrainingsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrainingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'INSTRUCTOR':
            return Training.objects.filter(instructor_id=user.uuid)
        elif user.role == 'SOLDIER':
            return Training.objects.filter(soldiers=user)
        else:
            return Response({'detail': 'Invalid user role'}, status=status.HTTP_400_BAD_REQUEST)