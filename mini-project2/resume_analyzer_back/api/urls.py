from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('password_reset/confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('upload_resume/', views.upload_resume, name='upload_resume'),
    path('resumes/', views.ResumeListView.as_view(), name='resume_list'),
    path('specializations/', views.get_specializations, name='get_specializations'),
]
