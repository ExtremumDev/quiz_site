from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import DriverForm
from .models import Slide, Driver, TestResult
from .test_config import QUESTIONS
from .utils import serialize_user_test_result


# Create your views here.

class RegisterDriverView(CreateView):
    model = Driver
    form_class = DriverForm
    template_name = "quiz/driver_reg.html"
    success_url = reverse_lazy("reg_driver")

    def form_valid(self, form):

        response = super().form_valid(form)

        self.request.session["driver_id"] = self.object.pk

        return response


def slide_view(request: HttpRequest, slide_number: int):
    slide = get_object_or_404(Slide, number=slide_number)

    prev_slide = Slide.objects.filter(number__lt=slide_number).last()
    next_slide = Slide.objects.filter(number__gt=slide_number).first()

    return render(request, "quiz/slide.html", {
        "slide": slide,
        "prev_slide": prev_slide,
        "next_slide": next_slide,
    })

def test(request: HttpRequest):
    driver_id = request.session.get("driver_id")

    if driver_id:
        try:
            driver = Driver.objects.get(pk=driver_id)
        except Driver.DoesNotExist:
            return redirect(reverse("reg_driver"))
        if request.method == "POST":

            answers = []
            score = 0

            for i, q in enumerate(QUESTIONS):
                answer = int(request.POST.get(f"q{i}"))
                answers.append(answer)

                if answer == q["correct"]:
                    score += 1

            TestResult.objects.create(
                driver=driver,
                q1=answers[0],
                q2=answers[1],
                q3=answers[2],
            )


            return redirect(reverse("result"))


        return render(request, "quiz/test.html", {"questions": QUESTIONS})
    else:
        return redirect(reverse("reg_driver"))

def self_result_view(request):
    driver_id = request.session.get("driver_id")

    if driver_id:
        try:
            driver = Driver.objects.get(pk=driver_id)
        except Driver.DoesNotExist:
            return redirect(reverse("reg_driver"))

        user_result = TestResult.objects.filter(driver=driver).first()
        if user_result:

            results = serialize_user_test_result(QUESTIONS, user_result)

            return render(request, "quiz/result.html", {
                "full_name": driver.full_name,
                "results": results
            })
        else:
            return redirect(reverse("test"))
    else:
        return redirect(reverse("reg_driver"))

@staff_member_required
def users_result_view(request: HttpRequest):
    users = Driver.objects.filter(test__isnull=False)

    return render(request, "quiz/driver_reg.html", context={"users": users})

@staff_member_required
def certain_user_result(request: HttpRequest, user_id: int):
    user = get_object_or_404(Driver, pk=user_id)

    user_result = TestResult.objects.filter(driver=user).first()

    if user_result:
        results = serialize_user_test_result(QUESTIONS, user_result)

        return render(
            request,
            "quiz/result.html",
            {
                "full_name": user.full_name,
                "results": results
            }
        )
    else:
        raise Http404("Пользователь не проходил тестирование")


def index(request: HttpRequest):
    return render(request, "index.html")
