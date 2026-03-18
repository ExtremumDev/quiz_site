from django.db import models

# Create your models here.

class Driver(models.Model):
    surname = models.CharField(verbose_name="Фамилия", max_length=255)
    first_name = models.CharField(verbose_name="Имя", max_length=255)
    patronymic = models.CharField(verbose_name="Отчество", max_length=255, blank=True, default="")
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=12)
    position = models.CharField(verbose_name="Должность", max_length=50)

    @property
    def full_name(self):
        return f"{self.surname} {self.first_name} {self.patronymic}"


class Slide(models.Model):
    title = models.CharField(max_length=200, blank=True, default="")
    video = models.FileField(upload_to="video_lessons/")
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"{self.number}. {self.title}"

    class Meta:
        ordering = ["number"]

        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"


class Question(models.Model):
    content = models.CharField(verbose_name="Вопрос", max_length=400)
    options = models.JSONField(
        verbose_name="Варианты ответов"
    ) # [{'id': <choice_id>, 'text': <choice_text>}]
    correct = models.PositiveIntegerField()
    number = models.PositiveIntegerField(verbose_name="Номер вопроса", unique=True, null=True)


class Answer(models.Model):
    question = models.ForeignKey(to="Question", on_delete=models.CASCADE, related_name="answers")
    attempt = models.ForeignKey(to="Attempt", on_delete=models.CASCADE, related_name="answers")
    selected = models.PositiveIntegerField(verbose_name="Выбранный ответ")

    class Meta:
        ordering = ["question__number"]


class Attempt(models.Model):
    driver = models.ForeignKey(to="Driver", on_delete=models.SET_NULL, related_name="attempts", null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TestResult(models.Model):
    driver = models.OneToOneField("Driver", on_delete=models.CASCADE, related_name="test")
    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()