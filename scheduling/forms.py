from django import forms

class EventForm(forms.Form):
    title = forms.CharField(max_length=100)
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
