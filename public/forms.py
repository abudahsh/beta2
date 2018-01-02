from django import forms

from public.models import ServiceProvider, Review


class ServiceCreationForm(forms.ModelForm):

    class Meta:
        model= ServiceProvider
        fields= ['name',  'description', 'photo', 'location', 'website']

class ReviewCreationForm(forms.ModelForm):

    class Meta:
        model=Review
        fields=['body', 'rate']