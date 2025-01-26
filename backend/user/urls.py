from django.urls import path
from .views import UserRegisterView, login_user, getData, updateData, getStats, updatePhoto

urlpatterns = [
    path('register/', UserRegisterView, name='register'),
    path('login/', login_user, name='login'),
    path('getData/', getData, name='get_data'),
    path('updateData/', updateData, name='update_data'),
    path('getStats/', getStats, name='get_stats'),
    path('updatePhoto/', updatePhoto, name='updatePhoto'),
]