from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from djangoapp.models import Mine
from ..serializers import MineUpdateSerializer

class UpdateMineAPIView(APIView):
    def put(self, request):
        mine_uuid = request.headers.get('uuid')
        if not mine_uuid:
            return Response({"detail": "Missing uuid in headers."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mine = Mine.objects.get(uuid=mine_uuid)
        except Mine.DoesNotExist:
            return Response({"detail": "Mine not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MineUpdateSerializer(mine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)