from django.urls import path
from app1 import views

app_name = 'app1'


urlpatterns = [
    path('signUp/', views.signUp),
    path('logIn/', views.logIn),
    path('userVerifySendOTP/', views.userVerifySendOTP),
    path('userVerifyOTP/', views.userVerifyOTP),
    path('uploadFile/', views.uploadFile),
    path('uploads/', views.getAllFiles),
    path('download/', views.downloadRequest),
    path('download-file/<str:download_file_id>/', views.download_file),
    path('share/', views.shareFile),
    path('shared/', views.sharedFiles)

]