from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class SubLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class UserLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)


class Quiz(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class SubQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    subQuiz = models.ForeignKey(SubQuiz, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)


class QuizResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correctAnswers = models.DecimalField(max_digits=2000, decimal_places=0)
    created_date = models.DateTimeField(auto_now_add=True)
