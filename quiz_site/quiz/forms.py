from typing import List

from django import forms

from .models import Driver, Answer, Attempt


class DriverForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("first_name", "surname", "patronymic", "phone_number", "position")


class TestForm:

    def __init__(self, data: dict):
        self.data = data
        self.answers: List[Answer] = []
        self.test_attempt: Attempt = None

    def create_attempt(self, driver: Driver):
        self.test_attempt = Attempt(driver=driver)
        self.test_attempt.save()

        for k, v in self.data.items():
            question_info = k.split('_') # votes n POST: {'q_1': '<answer1>', 'q_2': '<answer2>', ...}

            if len(question_info) == 2:
                try:
                    question_id = int(question_info[0])

                    answer_id = int(question_info[0])

                    self.answers.append(Answer(selected=answer_id, question_id=question_id, attempt=self.test_attempt))
                except ValueError:
                    continue

    def save_attempt(self):
        try:
            Answer.objects.add(*self.answers)
        except Exception:
            self.test_attempt.delete()

