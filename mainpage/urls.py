from django.urls import path
from .views import (home, JobListView, JobDetailView,
                    JobCreateView, JobUpdateView, JobDeleteView,
                    LocationListView, EmployerListView, StatusListView)

urlpatterns = [
    path('', home, name="home"),
    path('job/', JobListView.as_view(), name="job-home"),
    path('job/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('job/new/', JobCreateView.as_view(), name='job-create'),
    path('job/<int:pk>/update', JobUpdateView.as_view(), name='job-update'),
    path('job/<int:pk>/delete', JobDeleteView.as_view(), name='job-delete'),
    path('location/<str:state>/<str:city>',
         LocationListView.as_view(), name="location-jobs"),
    path('employer/<str:employer>',
         EmployerListView.as_view(), name="employer-jobs"),
    path('status/<str:status>', StatusListView.as_view(), name="status-jobs"),
]
