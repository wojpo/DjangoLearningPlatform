from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from .models import Course, Lesson, UserLesson, SubLesson, Quiz, SubQuiz, Answer, QuizResults
from django.views.generic import DetailView


class CourseDetailView(DetailView):
    @method_decorator(login_required(login_url='/loginpage'))
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        lessons = Lesson.objects.filter(course=course)
        if_completed = UserLesson.objects.filter(lesson__course=course)
        lessons_num = len(lessons)
        return render(request, 'course.html', {'course': course, 'lessons': lessons, 'lessons_count': lessons_num,
                                               'if_completed': if_completed})


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


class QuizDetailView(DetailView):
    @method_decorator(login_required(login_url='/loginpage'))
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        subquizes = SubQuiz.objects.filter(quiz=quiz)
        return render(request, 'quiz.html', {'quiz': quiz, 'subquizes': subquizes})

    @method_decorator(login_required(login_url='/loginpage'))
    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        request.session['quiz_id'] = quiz.id
        request.session['current_question'] = 0
        request.session['correct_answers'] = 0
        first_subquiz = SubQuiz.objects.filter(quiz=quiz).first()
        if first_subquiz:
            return redirect('subquiz-detail', quiz_pk=quiz.id, pk=first_subquiz.id)
        else:
            return redirect('quiz-detail', pk=quiz.id)


class SubQuizDetailView(DetailView):
    @method_decorator(login_required(login_url='/loginpage'))
    def get(self, request, quiz_pk, pk):
        subquiz = get_object_or_404(SubQuiz, pk=pk)
        answers = Answer.objects.filter(subQuiz=subquiz)
        return render(request, 'subquiz.html', {'subquiz': subquiz, 'answers': answers})


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
def vote(request, quiz_pk, pk):
    subquiz = get_object_or_404(SubQuiz, pk=pk, quiz_id=quiz_pk)
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    sub_quizzes = SubQuiz.objects.filter(quiz=quiz)

    if request.method == 'POST':
        try:
            selected_answer = subquiz.answer_set.get(pk=request.POST['answer'])
        except (KeyError, Answer.DoesNotExist):
            return render(request, 'subquiz.html', {
                'subquiz': subquiz,
                'answers': Answer.objects.filter(subQuiz=subquiz),
                'error_message': "You didn't select a choice.",
            })

        if 'correct_answers' not in request.session:
            request.session['correct_answers'] = 0

        if selected_answer.is_correct:
            request.session['correct_answers'] += 1

        current_question = request.session.get('current_question', 0) + 1
        request.session['current_question'] = current_question

        if current_question >= len(sub_quizzes):
            return redirect('results', quiz_pk=quiz_pk)
        else:
            next_subquiz = sub_quizzes[current_question]
            return redirect('subquiz-detail', quiz_pk=quiz_pk, pk=next_subquiz.pk)


@login_required(login_url='/loginpage')
def quiz_results(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    correct_answers = request.session.get('correct_answers', 0)
    result = QuizResults(quiz=quiz, user=request.user, correctAnswers=correct_answers)
    result.save()
    return render(request, 'result.html', {'result': result})


@login_required(login_url='/loginpage')
def mark_lesson_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    user = request.user
    UserLesson.objects.get_or_create(user=user, lesson=lesson, defaults={'completed': True})
    course_id = lesson.course.id
    return HttpResponseRedirect(reverse('course-detail', args=[course_id]))
