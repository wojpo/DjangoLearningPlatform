from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from .models import Course, Lesson, UserLesson, SubLesson
from django.views.generic import DetailView


class CourseDetailView(DetailView):
    @method_decorator(login_required(login_url='/loginpage'))
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        lessons = Lesson.objects.filter(course=course)
        lessons_num = len(lessons)
        return render(request, 'course.html', {'course': course, 'lessons': lessons, 'lessons_count': lessons_num})


class LessonDetailView(DetailView):
    @method_decorator(login_required(login_url='/loginpage'))
    def get(self, request, course_pk, pk):
        lesson = get_object_or_404(Lesson, pk=pk, course_id=course_pk)

        if lesson.course.pk != course_pk:
            raise Http404("Lesson not found")

        user = request.user
        try:
            user_lesson = UserLesson.objects.get(user=user, lesson=lesson)
            completed = user_lesson.completed
        except UserLesson.DoesNotExist:
            completed = False
        subLessons = SubLesson.objects.filter(lesson=lesson)

        return render(request, 'lesson.html', {'lesson': lesson, 'completed': completed, 'sublessons': subLessons})


@login_required(login_url='/loginpage')
def courses(request):
    all_courses = Course.objects.all()
    if_user_completed = {}
    user = request.user
    for course in all_courses:
        for lesson in course.lesson_set.all():
            if UserLesson.objects.filter(user=user, lesson=lesson).exists():
                UwU = UserLesson.objects.get(user=user, lesson=lesson)
                if_user_completed[lesson.pk] = UwU.completed

    return render(request, 'courses.html', {'courses': all_courses, 'if_completed': if_user_completed})


@login_required(login_url='/loginpage')
def mark_lesson_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    user = request.user
    UserLesson.objects.get_or_create(user=user, lesson=lesson, defaults={'completed': True})
    course_id = lesson.course.id
    return HttpResponseRedirect(reverse('course-detail', args=[course_id]))
