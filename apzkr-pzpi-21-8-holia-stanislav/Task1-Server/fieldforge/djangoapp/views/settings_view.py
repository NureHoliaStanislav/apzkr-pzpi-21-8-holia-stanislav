from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.generics import RetrieveUpdateAPIView # type: ignore 
from rest_framework.permissions import IsAuthenticated # type: ignore
from ..serializers import  SettingsSerializer

class SettingsRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SettingsSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user.settings)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('settings', {})

        serializer = self.serializer_class(
            request.user.settings, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)