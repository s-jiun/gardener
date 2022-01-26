from django import forms
from .models import Plant, Plant_register


class PlantWikiForm(forms.ModelForm):
    class Meta:
        model = Plant_register
        fields = ["name", "photo", "growth_form", "management_level","water_period_spring","water_period_summer","water_period_autumn","water_period_winter","growth_temp","sunlight","humidity","flower","content"]
