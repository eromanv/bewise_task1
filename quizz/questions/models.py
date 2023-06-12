from django.db import models


class Question_quiz(models.Model):
    question = models.CharField(max_length=256)
    id = models.IntegerField(primary_key=True)
    answer = models.CharField(max_length=256)
    created_at = models.DateField()

    def __str__(self):
        return self.question
