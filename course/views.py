
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Course, Question, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        'course/course_details_bootstrap.html',
        {'course': course}
    )


@login_required
def exam(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        'course/exam.html',
        {'course': course}
    )


@login_required
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    questions = Question.objects.filter(course=course)

    score = 0
    total = 0

    for question in questions:
        total += question.grade

        selected_choice = request.POST.get(
            f'question_{question.id}'
        )

        if selected_choice:
            correct_choice = question.choices.filter(
                is_correct=True
            ).first()

            if correct_choice and str(correct_choice.id) == selected_choice:
                score += question.grade

    submission = Submission.objects.create(
        user=request.user,
        course=course,
        score=score,
        total=total
    )

    return redirect(
        'show_exam_result',
        course_id=course.id,
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        user=request.user,
        course=course
    )

    return render(
        request,
        'course/exam_result.html',
        {
            'course': course,
            'submission': submission
        }
    )