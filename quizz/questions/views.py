from django.shortcuts import render
from django.http import JsonResponse
from .api import get_quiz_questions

def home(request):
    if request.method == "POST":
        questions_num = request.POST.get("questions_num")
        data = get_quiz_questions(questions_num)
        return JsonResponse(data)
    return render(request, "home.html")