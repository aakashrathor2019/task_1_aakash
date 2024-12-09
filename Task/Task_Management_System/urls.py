from django.urls import path
from .views import *

urlpatterns=[
  path('login/',Login.as_view(),name='login'),
  path('signup/',Signup.as_view(),name='signup'),
  path('create_task/',Create_Task.as_view(),name='create_task'),

]