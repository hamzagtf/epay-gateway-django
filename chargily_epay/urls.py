from django.urls import path
from .views import home, done_page
urlpatterns = [
    path('', home),
    path('done_page/', done_page),
    
]