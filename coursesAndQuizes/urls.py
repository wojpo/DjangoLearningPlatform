from django.urls import path
from .views import CourseDetailView, LessonDetailView, mark_lesson_complete, courses, QuizDetailView, SubQuizDetailView, vote, quiz_results, quizes, overview, all_quiz_results

urlpatterns = [
    path('', overview, name='overview'),
    path('courses/', courses, name='courses'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('course/<int:course_pk>/lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('quizes/', quizes, name='quizes'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/<int:quiz_pk>/subquiz/<int:pk>', SubQuizDetailView.as_view(), name='subquiz-detail'),
    path('quiz/<int:quiz_pk>/subquiz/<int:pk>/vote', vote, name='vote'),
    path('quiz/<int:quiz_pk>/results', quiz_results, name='results'),
    path('mark-lesson-complete/<int:lesson_id>/', mark_lesson_complete, name='mark_lesson_complete'),
    path('quiz/results', all_quiz_results, name='all-results')
]
