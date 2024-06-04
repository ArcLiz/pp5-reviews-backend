from django.urls import path
from followers import views
from .views import follow_user

urlpatterns = [
    path('followers/', views.FollowerList.as_view()),
    path('followers/<int:pk>/', views.FollowerDetail.as_view()),
    path('follow/<int:followed_id>/', follow_user, name='follow_user'),
]
