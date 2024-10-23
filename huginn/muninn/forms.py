from .models import Chapter
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['pdf','grade','chapter','subject']  


class QuestionAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuestionAnswerForm, self).__init__(*args, **kwargs)
        for i in range(15):
            self.fields[f'answer{i+1}'] = forms.CharField(label=f'Answer {i+1}', max_length=1000) # Simpler to add all 15 answers dynamically

