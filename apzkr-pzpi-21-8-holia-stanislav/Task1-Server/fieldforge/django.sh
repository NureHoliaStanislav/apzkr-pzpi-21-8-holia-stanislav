#!/bin/bash

# Wait for Postgres to be ready
chmod +x wait-for-postgres.sh
./wait-for-postgres.sh db

source ./fieldforge.env

echo "Creating Migrations..."
python manage.py makemigrations djangoapp
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

# echo "Creating Super User..."
# if [ "$DJANGO_SUPERUSER_EMAIL" ]
# then
#     echo "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').exists())" | python manage.py shell | grep -q "False"
#     if [ $? -eq 0 ]
#     then
#         echo "from django.contrib.auth import get_user_model; \
#          User = get_user_model(); User.objects.create_superuser \
#          ('$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" \
#          | python manage.py shell
#         echo "Superuser created."
#     else
#         echo "Superuser already exists. Skipping creation."
#     fi
# fi

# echo ====================================

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000




