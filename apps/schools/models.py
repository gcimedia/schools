from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class School(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} ({self.school.name})"

    class Meta:
        unique_together = ("school", "order")
        ordering = ["school", "order"]


class Enrollment(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"role": "student"}
    )
    module = models.ForeignKey(Unit, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} in {self.module.title}"

    class Meta:
        unique_together = ("student", "module")
