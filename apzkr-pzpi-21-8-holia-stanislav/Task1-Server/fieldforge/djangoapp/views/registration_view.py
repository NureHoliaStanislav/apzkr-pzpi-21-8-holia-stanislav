from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.permissions import AllowAny # type: ignore
from rest_framework.views import APIView # type: ignore
from ..renderers import UserJSONRenderer
from ..serializers import RegistrationSerializer

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    