from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

class Driver(models.Model):
    surname = models.CharField(verbose_name="Фамилия", max_length=255)
    first_name = models.CharField(verbose_name="Имя", max_length=255)
    patronymic = models.CharField(verbose_name="Отчество", max_length=255, blank=True, default="")
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=12)
    position = models.CharField(verbose_name="Должность", max_length=50)


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

class TestResult(models.Model):
    driver = models.OneToOneField("Driver", on_delete=models.CASCADE, related_name="test")

    created_at = models.DateTimeField(auto_now_add=True)

    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()
