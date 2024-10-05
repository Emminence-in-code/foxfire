from django.db import models
from custom_auth.models import CustomUser
import random, string
from django.core.exceptions import ValidationError

from api.transacions import deposit
from notifications_and_messages.models import send_notification
from forgot_password.generate_token import generate_token

submit_types = (("image", "Image"), ("code", "Code"))


# Create your models here.
class Task(models.Model):
    task_name = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_created=True)
    link = models.URLField()
    completed = models.ManyToManyField(CustomUser)
    reward = models.IntegerField(default=0)
    submit_type = models.CharField(max_length=50, choices=submit_types, default="image")

    def __str__(self):
        return self.task_name


class TaskSubmit(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    proof_of_work = models.CharField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        # make sure the upload type matches the task type

        if self.confirmed:
            # credit user with the task rewards
            self.task.completed.add(self.user)
            self.task.save()
            rewards = self.task.reward
            deposit(wallet=self.user.wallet_set.first(), amount=rewards)
            send_notification(
                title="Task completed",
                user=self.user,
                notification=f"You have earned {rewards} flame tokens for completing task",
            )
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task.task_name} submit request from {self.user}"


class Category(models.Model):
    image = models.ImageField(upload_to="category")
    category = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class Survey(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="surveys")
    description = models.TextField()
    reward = models.IntegerField(default=0)
    upload_complete = models.BooleanField(default=False)

    def get_total_questions_count(self):
        return self.questions.count()

    def get_answered_questions_count(self, user):
        return UserResponse.objects.filter(user=user, question__survey=self).count()

    def save(self, *args, **kwargs):
        # Prevent saving if the survey is already marked as complete
        if self.pk is not None:  # Check if the object already exists in the database
            original = Survey.objects.get(pk=self.pk)
            if original.upload_complete:
                raise ValidationError(
                    "This survey is no longer editable as it has been marked complete."
                )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    order = models.IntegerField(default=0, blank=True, null=True)
    option = models.TextField(blank=True, null=True)
    option2 = models.TextField(blank=True, null=True)
    option3 = models.TextField(blank=True, null=True)
    option4 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.survey.title} - Question {self.order}"


class UserResponse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "question"]

    def __str__(self):
        return f"{self.user.username}'s response to {self.question}"


class SurveyCompletion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["user", "survey"]

    def __str__(self):
        status = "Completed" if self.completed else "In Progress"
        return f"{self.user.username}'s {status} - {self.survey.title}"

    @classmethod
    def get_completed_surveys_count(cls, user):
        return cls.objects.filter(user=user, completed=True).count()


class WithdrawRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=1, max_digits=20)
    bank_description = models.TextField()
    account_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} wants to withdraw {self.amount}"


class ExchangeRate(models.Model):
    points = models.DecimalField(default=1000.00, decimal_places=4, max_digits=20)
    amount = models.DecimalField(default=1, decimal_places=4, max_digits=20)


class Referral(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, blank=True, null=True)
    used_count = models.IntegerField(default=0)

    def use_code(self):
        used_count += 1
        self.save()

    @staticmethod
    def generate_code() -> int:

        numbers = random.sample(range(1, 9), 6)
        return generate_token(6, False)

    def save(self, *args, **kwargs) -> None:
        if not self.code:
            self.code = self.generate_code()
        return super().save(*args, **kwargs)
