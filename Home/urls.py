from django.urls import path , include
from . import views

urlpatterns = [
    
    path('', views.index ,name='index'),
    path('signup/', views.signup ,name='signup'),
    path('signup-student/', views.signup_student ,name='signup-student'),

    path('posts/', views.Courses ,name='course_all'),
    path('<int:id>/', views.Coursedetail ,name='detail'),
    path('<str:category>/', views.category ,name='category'),
]
