from django.db import models
from custom_auth.models import CustomUser
import random, string


# Create your models here.
class Task(models.Model):
    task_name = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_created=True)
    link = models.URLField()
    completed = models.ManyToManyField(CustomUser)
    reward = models.IntegerField(default=0)
    # TODO implement task submission


class Category(models.Model):
    image = models.ImageField(upload_to="category")
    category = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"


class Survey(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="surveys")
    description = models.TextField()
    reward = models.IntegerField(default=0)

    def get_total_questions_count(self):
        return self.questions.count()

    def get_answered_questions_count(self, user):
        return UserResponse.objects.filter(user=user, question__survey=self).count()


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


class Announcement(models.Model):
    image = models.ImageField(
        upload_to="images", help_text="icon image for announcement"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()


class WithdrawRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=4, max_digits=8)
    bank_description = models.TextField()
    account_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class ExchangeRate(models.Model):
    points = models.DecimalField(default=1000.00, decimal_places=4, max_digits=8)
    amount = models.DecimalField(default=1, decimal_places=4, max_digits=8)


class Referral(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, blank=True, null=True)
    used_count = models.IntegerField(default=0)

    def use_code(self):
        used_count += 1
        self.save()

    @staticmethod
    def generate_code() -> int:

        numbers = random.sample(range(1, 46), 6)
        return int("".join(map(str, sorted(numbers))))

    def save(self, *args, **kwargs) -> None:
        if not self.code:
            self.code = self.generate_code()
            print(self.code)
            
        return super().save(*args, **kwargs)
