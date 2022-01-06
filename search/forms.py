from django import forms
from .models import Plant


class PlantWikiForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "photo_url", "growth_form", "care_difficulty", "management_level","water_period_spring","water_period_summer","water_period_autumn","water_period_winter","growth_temp","sunlight","humidity","flower","content"]
