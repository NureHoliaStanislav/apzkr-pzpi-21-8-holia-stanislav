from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.permissions import AllowAny # type: ignore
from rest_framework.views import APIView # type: ignore
from ..renderers import UserJSONRenderer
from ..serializers import LoginSerializer

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)