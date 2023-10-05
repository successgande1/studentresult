from django.urls import path

from . import views

urlpatterns = [
    path('create/subject/', views.create_subject, name='class-subject'),
]