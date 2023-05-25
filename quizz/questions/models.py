from django.db import models

"""
: 1. ID вопроса, 2. Текст вопроса, 3. Текст ответа, 4. - Дата создания вопроса 
"""


class Question_quiz(models.Model):
    question = models.CharField()
    id = models.IntegerField(primary_key=True)
    answer = models.CharField()
    created_at = models.DateField()

    def __str__(self):
        return self.question
