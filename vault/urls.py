from django.urls import path
from .views.candidate import register, list_candidates, download_resume

urlpatterns = [
    path('candidate/register', register, name='register_candidate'),
    path('candidate/list', list_candidates, name='list_candidates'),
    path('candidate/download/<int:candidate_id>', download_resume, name='download_resume'),
]