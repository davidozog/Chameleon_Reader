from django.forms import ModelForm
from notes.models import Notes

class PartialNotesForm(ModelForm):
    class Meta:
        model = Notes 
        exclude = ('user',)
