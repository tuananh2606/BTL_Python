from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('timesheet/', views.view_timesheet, name='timesheet'),
  path('<int:id>', views.view_student, name='view_student'),
  path('add/', views.add, name='add'),
  path('edit/<int:id>/', views.edit, name='edit'),
  path('delete/<int:id>/', views.delete, name='delete'),
]