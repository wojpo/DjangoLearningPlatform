from django.contrib import admin
from .models import Course, Lesson, UserLesson, SubLesson

# Register your models here.


admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(UserLesson)
admin.site.register(SubLesson)