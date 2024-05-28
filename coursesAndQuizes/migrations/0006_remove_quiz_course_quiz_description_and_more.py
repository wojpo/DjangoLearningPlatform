# Generated by Django 5.0.4 on 2024-05-28 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursesAndQuizes', '0005_course_created_date_userlesson_created_date_quiz_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='course',
        ),
        migrations.AddField(
            model_name='quiz',
            name='description',
            field=models.TextField(default='dsa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subquiz',
            name='question',
            field=models.CharField(max_length=200),
        ),
    ]