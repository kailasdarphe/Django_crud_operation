from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib import messages
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ChatMessage

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, "students/add.html", {'form': form})


def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/edit.html', {'form': form})

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "Record deleted successfully!")
    return redirect('student_list')

# --------------------
# RASA CHATBOT VIEWS
# --------------------

def chatbot_page(request):
    return render(request, "chatbot/chat.html")

@csrf_exempt
def rasa_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_msg = data.get("message")

        # Save USER message
        ChatMessage.objects.create(sender="user", message=user_msg)

        # Send to rasa
        rasa_response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "user", "message": user_msg}
        )

        bot_reply = rasa_response.json()[0]["text"]

        # Save BOT message
        ChatMessage.objects.create(sender="bot", message=bot_reply)

        return JsonResponse({"reply": bot_reply})