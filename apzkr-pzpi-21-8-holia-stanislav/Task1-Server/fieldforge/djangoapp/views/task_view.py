from rest_framework import generics, status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from ..serializers.task_serializer import TaskSerializer
from ..models import Instructor, Task

class TaskCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        if not Instructor.objects.filter(user_ptr_id=request.user.uuid).exists():
            return Response({"detail": "Only instructors can create task."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class TaskDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    lookup_field = 'uuid'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.training.instructor.user_ptr_id != request.user.uuid:
            return Response({"detail": "Only the instructor who created the task can delete it."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TaskUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    lookup_field = 'uuid'
    queryset = Task.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.training.instructor.user_ptr_id != request.user.uuid:
            return Response({"detail": "Only the instructor who created the task can update it."}, status=status.HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)

class TaskRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'uuid'