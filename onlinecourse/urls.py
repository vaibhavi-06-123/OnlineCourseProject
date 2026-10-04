
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from course import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage redirect
    path('', lambda request: redirect('course_details', course_id=1), name='home'),

    # Course details
    path(
        'course/<int:course_id>/',
        views.course_details,
        name='course_details'
    ),

    # Exam page
    path(
        'course/<int:course_id>/exam/',
        views.exam,
        name='exam'
    ),

    # Submit exam
    path(
        'course/<int:course_id>/submit/',
        views.submit,
        name='submit'
    ),

    # Exam result
    path(
        'course/<int:course_id>/result/<int:submission_id>/',
        views.show_exam_result,
        name='show_exam_result'
    ),
]