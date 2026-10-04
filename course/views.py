from django.shortcuts import render, get_object_or_404
from .models import Course, Question, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        'course/course_details_bootstrap.html',
        {'course': course}
    )


def exam(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        'course/exam.html',
        {'course': course}
    )


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

    return render(
        request,
        'course/exam_result.html',
        {
            'course': course,
            'submission': submission
        }
    )


def show_exam_result(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    submission = Submission.objects.filter(
        user=request.user,
        course=course
    ).order_by('-submitted_at').first()

    return render(
        request,
        'course/exam_result.html',
        {
            'course': course,
            'submission': submission
        }
    )