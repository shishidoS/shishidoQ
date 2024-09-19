# inputapp/forms.py

from django import forms

class InputForm(forms.Form):
    text_input = forms.CharField(label='Your Input', max_length=100)
