from .login_view import LoginAPIView
from .registration_view import RegistrationAPIView
from .user_view import UserRetrieveUpdateAPIView, PublicUserRetrieveAPIView, DeactivateUserView, UserTrainingsView
from .settings_view import SettingsRetrieveUpdateAPIView
from .training_view import TrainingResultsView,CreateResultsView,TrainingDetailView,TrainingRetrieveView,TrainingCreateView,TrainingDeleteView, AddSoldiersToTrainingView, RemoveSoldiersFromTrainingView, TrainingUpdateView, AddMineView
from .task_view import TaskCreateView, TaskDeleteView, TaskUpdateView, TaskRetrieveView
from .admin_view import CreateAdminAPIView, UserListView, DeleteAdminAPIView, BanUserAPIView, CreateMineAPIView, DeleteMineAPIView, MineListView
from .mine_view import UpdateMineAPIView