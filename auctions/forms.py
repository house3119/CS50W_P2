from django import forms

from.models import Listing

class NewListingForm(forms.Form):
    title = forms.CharField(
        label="Title", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control new-li', 'placeholder': 'Required'})
        )
    
    selected_category = forms.ChoiceField(
        label="Select Category",
        choices=Listing.category_choices,
        initial="OT",
        widget=forms.Select(attrs={'class': 'form-control new-li'})
        )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control new-li', 'placeholder': 'Required'}),
        max_length=500
        )
    
    image_url = forms.URLField(
        label="Image URL (optional)", 
        required=False, 
        widget=forms.URLInput(attrs={'class': 'form-control new-li', 'placeholder': 'Optional'})
        )
    
    starting_bid = forms.IntegerField(
        min_value=0, 
        widget=forms.NumberInput(attrs={'class': 'form-control new-li', 'placeholder': 'Required'})
        )
