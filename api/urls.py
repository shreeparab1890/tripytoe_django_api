from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_home), #localhost:8000/api/
    path('itinerary/', views.generateItinerary) ,#localhost:8000/api/itinerary
    path('get/itinerary/', views.post_generateItinerary) #localhost:8000/api/get/itinerary
]
