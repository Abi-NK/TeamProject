try:
    from django import forms
    from core.models import Menu
except ImportError:
    print("failed import")

class AdjustMenuForm(forms.Form):

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
    cost = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Menu
        fields = ['name', 'price', 'description', 'course', 'category', 'allergy', 'calories', 'image', 'stock',
                  'vegetarian', 'vegan', 'meat', 'cost']
