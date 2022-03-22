from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.UserRegister.as_view(), name="register_user"),
    path("verify_user/", views.VerifyUser.as_view(), name="verify_user"),

]
