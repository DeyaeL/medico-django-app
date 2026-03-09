from django import forms
from .models import Consultation, Traitement

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        exclude = ['date']  
class TraitementForm(forms.ModelForm):
    class Meta:
        model = Traitement
        fields = ["medicament", "quantite", "contenant", "duree", "frequence", "posologie"]
