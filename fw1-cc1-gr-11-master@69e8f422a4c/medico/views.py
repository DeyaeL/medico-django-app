from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Consultation, Traitement
from .forms import ConsultationForm, TraitementForm
from django.db.models import Count
from django.db import models
from django.db.models.functions import TruncMonth

# end def import 


def home(request):
    return render(request, "medico/home.html")  

def about(request):
    return render(request, "medico/about.html", {"titre": "À propos de l'application Medico"})



def consultation_list(request):
    consultations = Consultation.objects.all().order_by('-id')
    return render(request, 'medico/consultation_list.html', {'consultations': consultations})

def consultation_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, "medico/consultation_detail.html", {"consultation": consultation})

def nouvelle_consultation(request):
    if request.method == "POST":
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            
            if hasattr(consultation, 'date'):
                consultation.date = timezone.now().date()
            elif hasattr(consultation, 'consultation_date'):
                consultation.consultation_date = timezone.now().date()
            consultation.save()
            return redirect("consultation_list")
    else:
        form = ConsultationForm()
    return render(request, "medico/nouvelle_consultation.html", {"form": form})

def changer_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    original_date = getattr(consultation, 'date', None) or getattr(consultation, 'consultation_date', None)

    if request.method == "POST":
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            obj = form.save(commit=False)
            if hasattr(obj, 'date') and original_date is not None:
                obj.date = original_date
            if hasattr(obj, 'consultation_date') and original_date is not None:
                obj.consultation_date = original_date
            obj.save()
            return redirect('consultation_detail', pk=consultation.pk)
    else:
        form = ConsultationForm(instance=consultation)

    return render(request, "medico/changer_consultation.html", {"form": form, "consultation": consultation})

def consultation_delete(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == "POST":
        consultation.delete()
        return redirect('consultation_list')
    return render(request, "medico/consultation_confirm_delete.html", {"consultation": consultation})


def ajouter_traitement(request, consultation_id):
    consultation = get_object_or_404(Consultation, pk=consultation_id)
    if request.method == "POST":
        form = TraitementForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.consultation = consultation
            t.save()
            return redirect("consultation_detail", pk=consultation.id)
    else:
        form = TraitementForm()
    return render(request, "medico/traitement_form.html", {"consultation": consultation, "form": form})

def modifier_traitement(request, pk):
    traitement = get_object_or_404(Traitement, pk=pk)
    consultation = traitement.consultation
    if request.method == "POST":
        form = TraitementForm(request.POST, instance=traitement)
        if form.is_valid():
            form.save()
            return redirect("consultation_detail", pk=consultation.id)
    else:
        form = TraitementForm(instance=traitement)
    return render(request, "medico/traitement_form.html", {"consultation": consultation, "traitement": traitement, "form": form})

def supprimer_traitement(request, pk):
    traitement = get_object_or_404(Traitement, pk=pk)
    consultation = traitement.consultation
    if request.method == "POST":
        traitement.delete()
        return redirect("consultation_detail", pk=consultation.id)
    return render(request, "medico/traitement_confirm_delete.html", {"consultation": consultation, "traitement": traitement})
def ordonnance_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    traitements = consultation.traitements.all()

    contexte = {
        "consultation": consultation,
        "traitements": traitements,
    }
    return render(request, "medico/ordonnance.html", contexte)

def patients_list(request):

    patients = (
        Consultation.objects
        .values("patient_nom", "patient_prenom", "patient_genre", "patient_age")
        .annotate(
            nb_consultations=Count("id"),
            example_id=models.Min("id"),  
        )
        .order_by("patient_nom", "patient_prenom")
    )

    contexte = {
        "patients": patients,
    }
    return render(request, "medico/patients_list.html", contexte)

def patient_history(request, consultation_id):

    consultation_ref = get_object_or_404(Consultation, pk=consultation_id)

    consultations_patient = (
        Consultation.objects
        .filter(
            patient_nom=consultation_ref.patient_nom,
            patient_prenom=consultation_ref.patient_prenom,
        )
        .order_by("-date")
        .prefetch_related("traitements")
    )

    contexte = {
        "patient_nom": consultation_ref.patient_nom,
        "patient_prenom": consultation_ref.patient_prenom,
        "patient_genre": consultation_ref.patient_genre,
        "patient_age": consultation_ref.patient_age,
        "consultations_patient": consultations_patient,
    }
    return render(request, "medico/patient_history.html", contexte)
def calculer_tendance_etat(consultations_queryset):
    """
    Calcule la tendance de l'état du patient sur les 3 dernières consultations.
    Retourne 'Amélioration', 'Dégradation', 'Stable' ou None.
    """
    derniers = list(consultations_queryset[:3])

    if len(derniers) < 2:
        return None  

    score_etat = {
        "Mauvais": 0,
        "Moyen": 1,
        "Bon": 2,
    }

    scores = [
        score_etat.get(c.etat_patient, 1)
        for c in reversed(derniers)
    ]

    if scores[-1] > scores[0]:
        return "Amélioration"
    elif scores[-1] < scores[0]:
        return "Dégradation"
    else:
        return "Stable"


def patient_history(request, consultation_id):

    consultation_ref = get_object_or_404(Consultation, pk=consultation_id)

    consultations_patient = (
        Consultation.objects
        .filter(
            patient_nom=consultation_ref.patient_nom,
            patient_prenom=consultation_ref.patient_prenom,
        )
        .order_by("-date")
        .prefetch_related("traitements")
    )

    tendance = calculer_tendance_etat(consultations_patient)
    stats = (
        Consultation.objects
        .filter(
            patient_nom=consultation_ref.patient_nom,
            patient_prenom=consultation_ref.patient_prenom,
        )
        .annotate(mois=TruncMonth("date"))
        .values("mois")
        .annotate(total=Count("id"))
        .order_by("mois")
    )

    labels = [s["mois"].strftime("%m/%Y") for s in stats]
    counts = [s["total"] for s in stats]

    contexte = {
        "patient_nom": consultation_ref.patient_nom,
        "patient_prenom": consultation_ref.patient_prenom,
        "patient_genre": consultation_ref.patient_genre,
        "patient_age": consultation_ref.patient_age,
        "consultations_patient": consultations_patient,
        "tendance": tendance,
        "labels": labels,
        "counts": counts,
    }
    return render(request, "medico/patient_history.html", contexte)
