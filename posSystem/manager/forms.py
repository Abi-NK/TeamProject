from django import forms
from customer.models import Menu
from django.core.exceptions import ValidationError


class AdjustMenuForm(forms.Form):

    id = forms.IntegerField()
    name = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=1000)
    course = forms.CharField(max_length=100)
    category = forms.CharField(max_length=100)
    allergy = forms.CharField(max_length=1000, required=False)
    calories = forms.IntegerField()
    image = forms.CharField(max_length=1000, required=False)
    stock = forms.IntegerField(min_value=0)
    vegetarian = forms.BooleanField(required=False)
    vegan = forms.BooleanField(required=False)
    meat = forms.BooleanField(required=False)

    class Meta:
        model = Menu
        fields = ['name', 'price', 'description', 'course', 'category', 'allergy', 'calories', 'image', 'stock',
                  'vegetarian', 'vegan', 'meat']
