from django.urls import path , include
from . import views

urlpatterns = [
    
    path('', views.index ,name='index'),
    path('signup/', views.signup ,name='signup'),
    path('<int:id>/', views.Coursedetail ,name='detail'),
    path('<str:category>/', views.category ,name='category'),
]
