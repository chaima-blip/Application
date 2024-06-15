# api/urls.py

# api/urls.py
from .views import validate_password
from .views import login
from django.urls import path
from . import views
from .views import (
    UserListCreate,
    UserRetrieveUpdateDestroy,
    UserRetrieveByID,
    UserRetrieveByEmail,
    UserUpdate,
    UserDelete,
    UserCreate
)

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='User-list-create'),
    path('users/<int:id>/', UserRetrieveUpdateDestroy.as_view(), name='User-retrieve-update-destroy'),
    path('users/id/<int:id>/', UserRetrieveByID.as_view(), name='User-retrieve-by-id'),
    path('users/email/<str:email>/', UserRetrieveByEmail.as_view(), name='User-retrieve-by-email'),
    path('users/update/<int:id>/', UserUpdate.as_view(), name='User-update'),
    path('users/delete/<int:id>/', UserDelete.as_view(), name='User-delete'),
    path('users/create/', UserCreate.as_view(), name='User-create'),
    path('users/validate-password/', validate_password, name='validate-password'),
    path('users/login/', login, name='login'),
    path('users/update/<str:email>/', views.UserUpdateByEmail.as_view(), name='user-update-by-email'),
    path('users/<str:email>/', views.UserRetrieveUpdateDestroyByEmail.as_view(), name='user-retrieve-update-destroy-by-email'),
      path('users/delete/<str:email>/', views.UserDeleteByEmail.as_view(), name='user-delete-by-email'),
]
    