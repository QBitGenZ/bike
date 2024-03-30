from django.urls import path

from user_management.views import AdminUserView, UserView, RegisterView, LoginView

urlpatterns = [
    path('admin-user/', AdminUserView.as_view()),
    path('user/', UserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
]