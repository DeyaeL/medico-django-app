from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('home/', views.home, name='home_page'),
    path('about/', views.about, name='about'),

    path('consultations/', views.consultation_list, name='consultation_list'),
    path('consultations/<int:pk>/', views.consultation_detail, name='consultation_detail'),
    path('nouvelle_consultation/', views.nouvelle_consultation, name='nouvelle_consultation'),
    path('changer_consultation/<int:pk>/', views.changer_consultation, name='changer_consultation'),
    path('effacer_consultation/<int:pk>/', views.consultation_delete, name='consultation_delete'),


    path('consultations/<int:consultation_id>/traitements/nouveau/', views.ajouter_traitement, name='ajouter_traitement'),
    path('traitements/<int:pk>/modifier/', views.modifier_traitement, name='modifier_traitement'),
    path('traitements/<int:pk>/supprimer/', views.supprimer_traitement, name='supprimer_traitement'),

     path(
        'consultations/<int:pk>/ordonnance/',
        views.ordonnance_consultation,
        name='ordonnance_consultation'
    ),
     path("patients/", views.patients_list, name="patients_list"),
    path(
        "patients/<int:consultation_id>/",
        views.patient_history,
        name="patient_history",
    ),
   
]
