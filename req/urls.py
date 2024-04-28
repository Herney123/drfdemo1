from django.urls import path
from . import views
urlpatterns = [
    path("students1/",views.StudentView.as_view()),
    path("students2/",views.StudentAPIView.as_view()),
]