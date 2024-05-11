from django.urls import path
from .views import CourseDetailView, LessonDetailView, mark_lesson_complete, courses

urlpatterns = [
    path('courses/', courses, name='courses'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('course/<int:course_pk>/lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('mark-lesson-complete/<int:lesson_id>/', mark_lesson_complete, name='mark_lesson_complete'),
]
