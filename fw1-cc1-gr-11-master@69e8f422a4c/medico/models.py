from django.db import models

class Consultation(models.Model):
    choix_genre = [
        ("M", "Masculin"),
        ("F", "Féminin"),
        ("Autre", "Autre"),
    ]
    
    patient_nom = models.CharField(max_length=40)
    patient_prenom = models.CharField(max_length=30)
    patient_genre = models.CharField(max_length=20, choices = choix_genre)
    patient_age = models.PositiveIntegerField()
    description = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.patient_nom} {self.patient_prenom}"

class Traitement(models.Model):
    consultation = models.ForeignKey(Consultation, related_name='traitements', on_delete=models.CASCADE)
    medicament = models.CharField(max_length=100)
    quantite = models.CharField(max_length=50)
    contenant = models.CharField(max_length=50)
    duree = models.PositiveIntegerField(help_text="Durée en jours")
    posologie = models.TextField(help_text="Détails de la posologie (ex : matin et soir)")
    frequence = models.CharField(max_length=50, help_text="ex: 2 fois par jour")

    def __str__(self):
        return f"{self.medicament} — {self.quantite} ({self.consultation})"