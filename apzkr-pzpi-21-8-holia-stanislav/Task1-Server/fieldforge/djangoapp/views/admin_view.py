from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework import generics # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.views import APIView # type: ignore
from ..permissions import IsStaffUser, IsSuperUser 
from ..renderers import UserJSONRenderer
from ..models import Mine, User
from ..serializers import AdminCreationSerializer, PublicUserSerializer, MineSerializer

class CreateAdminAPIView(APIView):
    permission_classes = (IsAuthenticated,IsSuperUser)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = AdminCreationSerializer

    def post(self, request):
        
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class DeleteAdminAPIView(APIView):
    permission_classes = (IsAuthenticated,IsSuperUser)

    def delete(self, request, uuid):
        try:
            user = User.objects.get(uuid=uuid, is_staff=True)
        except User.DoesNotExist:
            return Response({"detail": "Admin user not found."}, status=status.HTTP_404_NOT_FOUND)

        user.delete()

        return Response({"detail": "Admin user deleted."}, status=status.HTTP_204_NO_CONTENT)

class BanUserAPIView(APIView):
    permission_classes = (IsAuthenticated,IsStaffUser)

    def delete(self, request, uuid):
        try:
            user = User.objects.get(uuid=uuid, is_staff=False)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        User.objects.deactivate(user.uuid)

        return Response({"detail": "User is deactivated."}, status=status.HTTP_204_NO_CONTENT)


class UserListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsStaffUser)
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer       

class CreateMineAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,IsStaffUser)
    serializer_class = MineSerializer

    def post(self, request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class DeleteMineAPIView(APIView):
    permission_classes = (IsAuthenticated,IsStaffUser)

    def delete(self, request, uuid):
        try:
            mine = Mine.objects.get(uuid=uuid)
        except Mine.DoesNotExist:
            return Response({"detail": "Mine not found."}, status=status.HTTP_404_NOT_FOUND)

        mine.delete()

        return Response({"detail": "Mine deleted."}, status=status.HTTP_204_NO_CONTENT)

class MineListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsStaffUser)
    queryset = Mine.objects.all()
    serializer_class = MineSerializer  