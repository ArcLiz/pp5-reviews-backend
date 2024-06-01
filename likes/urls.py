from django.urls import path
from .views import LikeList, LikeDetails

urlpatterns = [

    path('likes/', LikeList.as_view()),
    path('likes/<int:pk>', LikeDetails.as_view()),
]
