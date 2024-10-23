from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from .forms import UploadFileForm,QuestionAnswerForm
from .models import *
from .helper import *
import os

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # save form through model form
            smt = Chapter.objects.all().last()
            
            smt.sut = summary('uploads/'+smt.t+'/'+os.listdir('uploads/'+smt.t+'/')[0])
            smt.fq, smt.fa = flashcard('uploads/'+smt.t+'/'+os.listdir('uploads/'+smt.t+'/')[0])
            
            smt.save()
            
            address = '/flashcard/'+smt.t
            return HttpResponseRedirect(address)  
    else:
        form = UploadFileForm()

    return render(request, "muninn/revision.html", {"form": form})

def fd(request, pk):
    #webpage for flashcard interface
    try:
        chapter = Chapter.objects.filter(identity=pk).first()
        flashcards = zip(chapter.fq, chapter.fa)  # Pair questions and answers together
        return render(request, "muninn/flashcard.html", {'flashcards': flashcards,'chapter':chapter})
    except Chapter.DoesNotExist:
        return HttpResponse('Chapter not found')

def flashmenu(request):
    #webpage for menu interface
    return render(request, "muninn/menu.html", {"chapters": Chapter.objects.all()})



        
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def quizzer(request,pk):
    try:
        chapter = Chapter.objects.get(identity=pk)
        question = questions('uploads/'+chapter.t+'/'+os.listdir('uploads/'+chapter.t+'/')[0])
        chapter.questions = question
        chapter.save()
        if request.method == "POST":
            form = QuestionAnswerForm(request.POST)
            if form.is_valid():
                chapter.answers = [form.cleaned_data[f'answer{i+1}'] for i in range(2)]
                chapter.save()
                return redirect("/graded"+f"/{pk}")
        else:
            form = QuestionAnswerForm()
        print(form.fields,len(chapter.questions))
        formlabels = zip(form.fields,chapter.questions)
        print([i for i in formlabels])
        return render(request,"muninn/quiz.html",{"form":form,"question":chapter.questions})
            
    except Chapter.DoesNotExist:
        return HttpResponse('Chapter not found')
            
def graded(request,pk):
    try: 
        chapter = Chapter.objects.get(identity=pk)
        grades,remarks = grade_list('uploads/'+chapter.t+'/'+os.listdir('uploads/'+chapter.t+'/')[0],chapter.answers,chapter.questions)

        print(len(grades),len(remarks),len(chapter.answers))
        return render(request,"muninn/graded.html",{"grades":grades,"remarks":remarks,"ans":chapter.answers})
    except Chapter.DoesNotExist:
        return HttpResponse("chapter does not exist :(")

def accountstats(request):
    render(request,"accstats.html")

def homepage(request):
    return render(request,"homepage.html",{"username":request.user.username})

