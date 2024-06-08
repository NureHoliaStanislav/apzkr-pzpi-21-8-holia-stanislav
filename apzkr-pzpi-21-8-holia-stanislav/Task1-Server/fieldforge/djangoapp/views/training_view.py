from datetime import datetime
from djangoapp.serializers.map_serializer import MapsMinesSerializer
from rest_framework import status # type: ignore
from rest_framework import generics # type: ignore
from django.db.models import Count, Q
from rest_framework.exceptions import ValidationError # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import action # type: ignore
from ..serializers import TrainingSerializer, ResultsSerializer, TrainingDetailSerializer
from ..models import Instructor, Map, MapsMines, Mine, Results, Training, Soldier
from rest_framework.permissions import IsAuthenticated # type: ignore

class TrainingCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrainingSerializer
        
    def post(self, request, *args, **kwargs):
        if not Instructor.objects.filter(user_ptr_id=request.user.uuid).exists():
            return Response({"detail": "Only instructors can create training."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        training = serializer.save()
        Map.objects.create(training=training)


class TrainingDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Training.objects.all()
    lookup_field = 'uuid'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.instructor.user_ptr_id != request.user.uuid:
            return Response({"detail": "Only the instructor who created the training can delete it."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AddSoldiersToTrainingView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrainingSerializer
    lookup_field = 'uuid'
    queryset = Training.objects.all()
        
    def post(self, request, uuid=None):
        training = self.get_object()
        soldiers = request.data.get('soldiers', [])
        if training.instructor.user_ptr_id != request.user.uuid:
            return Response({"detail": "Only the instructor who created the training can add soldiers."}, status=status.HTTP_403_FORBIDDEN)
    
        for soldier_uuid in soldiers:
            soldier = Soldier.objects.get(uuid=soldier_uuid)
            training.soldiers.add(soldier)

        training.save()

        return Response({"detail": "Soldiers added to training."}, status=status.HTTP_200_OK)
    

class RemoveSoldiersFromTrainingView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'
    queryset = Training.objects.all()

    def delete(self, request, uuid=None):
        training = self.get_object()
        soldiers = request.data.get('soldiers', [])
        
        if training.instructor.user_ptr_id != request.user.uuid:
            return Response({"detail": "Only the instructor who created the training can remove soldiers."}, status=status.HTTP_403_FORBIDDEN)

        for soldier_uuid in soldiers:
            soldier = Soldier.objects.get(uuid=soldier_uuid)
            training.soldiers.remove(soldier)

        training.save()

        return Response({"detail": "Soldiers removed from training."}, status=status.HTTP_200_OK)
    
class TrainingUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrainingSerializer
    lookup_field = 'uuid'
    queryset = Training.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.instructor.user_ptr_id != request.user.uuid:
            return Response({"detail": "Only the instructor who created the training can update it."}, status=status.HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)
    
class TrainingRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    lookup_field = 'uuid'

class AddMineView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = MapsMines.objects.all()
    serializer_class = MapsMinesSerializer

    def create(self, request, *args, **kwargs):
        mine_uuid = request.data.get('mine')
        if not mine_uuid:
            return Response({"detail": "Missing mine in request body."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            mine = Mine.objects.get(uuid=mine_uuid)
        except Mine.DoesNotExist:
            return Response({"detail": "Mine not found."}, status=status.HTTP_404_NOT_FOUND)

        training_uuid = self.kwargs['training_uuid']
        try:
            training = Training.objects.get(uuid=training_uuid)
            map = Map.objects.get(training=training)
        except (Training.DoesNotExist, Map.DoesNotExist):
            return Response({"detail": "Training or Map not found."}, status=status.HTTP_404_NOT_FOUND)

        if MapsMines.objects.filter(map=map, mine=mine).exists():
            return Response({"detail": "Mine is already added."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(map=map, mine=mine)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class TrainingDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Training.objects.all()
    serializer_class = TrainingDetailSerializer
    lookup_field = 'uuid'


class CreateResultsView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResultsSerializer
    lookup_field = 'uuid'
    queryset = Training.objects.all()

    def post(self, request, uuid=None):
        training = self.get_object()

        # Check if a Results object for the training already exists
        if Results.objects.filter(training=training).exists():
            raise ValidationError('Results for this training already exist')

        soldiers_lost = request.data.get('soldiers_lost', 0)

        # Iterate over the maps_mines relation and count the mines attributes for each related object
        mines_activated = training.map.mines.aggregate(activated=Count('is_activated', filter=Q(is_activated=True)))['activated']
        mines_defused = training.map.mines.aggregate(defused=Count('is_defused', filter=Q(is_defused=True)))['defused']
        total_mines = training.map.mines.count()
        mines_passed = total_mines - (mines_activated + mines_defused)

        # Check if end_time and start_time are both datetime objects and that end_time is later than start_time
        if not isinstance(training.end_time, datetime) or not isinstance(training.start_time, datetime):
            raise ValidationError('Invalid training times')

        if training.end_time is None or training.start_time is None:
            raise ValidationError('Both start_time and end_time must be non-null')

        if training.end_time < training.start_time:
            raise ValidationError('end_time must be later than start_time')

        # Calculate time_spent after checking that end_time and start_time are valid
        time_spent = training.end_time - training.start_time

        results_data = {
            'training': training.uuid,
            'mines_activated': mines_activated,
            'mines_passed': mines_passed,
            'mines_defused': mines_defused,
            'soldiers_lost': soldiers_lost,
            'time_spent': time_spent
        }

        serializer = self.get_serializer(data=results_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Calculate the success percentage
        total_mines = mines_activated + mines_passed + mines_defused
        if total_mines == 0:
            success_percentage = 0
        else:
            success_percentage = ((mines_defused + mines_passed) / total_mines) * 100

        # Subtract the ratio of soldiers_lost to total_mines from success_percentage
        if soldiers_lost > 0 and total_mines > 0:
            success_percentage -= (soldiers_lost / total_mines) * 100

        # Ensure success_percentage doesn't fall below 0
        success_percentage = max(success_percentage, 0)

        # Add the success percentage to the response data
        response_data = serializer.data
        response_data['success_percentage'] = success_percentage


        return Response(response_data, status=status.HTTP_201_CREATED)
    
class TrainingResultsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResultsSerializer
    queryset = Training.objects.all()
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object().results
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        # Calculate the success percentage
        total_mines = instance.mines_activated + instance.mines_passed + instance.mines_defused
        if total_mines == 0:
            success_percentage = 0
        else:
            success_percentage = ((instance.mines_defused + instance.mines_passed) / total_mines) * 100

        # Subtract the ratio of soldiers_lost to total_mines from success_percentage
        if instance.soldiers_lost > 0 and total_mines > 0:
            success_percentage -= (instance.soldiers_lost / total_mines) * 100

        # Ensure success_percentage doesn't fall below 0
        success_percentage = max(success_percentage, 0)

        return Response({
            'results': response_data,
            'success_percentage': success_percentage
        })
