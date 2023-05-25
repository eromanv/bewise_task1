from django.shortcuts import render
from django.http import JsonResponse
from .models import Question_quiz

def get_question(request, pk):
    if request.method == 'GET':
        
