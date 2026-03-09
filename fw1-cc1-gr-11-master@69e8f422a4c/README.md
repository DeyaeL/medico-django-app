- Deyae Lesdif — L3 MIAGE deyae.lesdif@etu.univ-orleans.fr
- Wissal OUCHEN L3 MIAGE wissal.ouchen@etu.univ-orleans.fr
- Rania ZAKRAF L3 MIAGE rania.zakraf@etu.univ-orleans.fr
- Abir Es-Saiydy - L3 MIAGE abir.es-saiydy@etu.univ-orleans.fr



## Question 1 - commandes
- django-admin startproject cc .  
- python manage.py startapp medico  
- python manage.py migrate

## Question 2 – Page /about/
Fichiers modifiés :
- medico/views.py : ajout de la vue `about`
- medico/templates/medico/about.html : création du template
- cc/urls.py : ajout de la route `/about/`

## Commandes utilisées :

docker compose up
docker exec -it fw1-cc1 bash
python manage.py runserver 0.0.0.0:8000
- docker compose up
- docker exec -it fw1-cc1 bash
- python manage.py runserver 0.0.0.0:8000

## Question 3
### Commandes utilisées
- python manage.py makemigrations medico
- python manage.py migrate
- python manage.py shell
- from medico.models import Consultation
- from datetime import date
- Consultation.objects.all()

### Justification des choix
- `CharField` utilisé pour les noms et prénoms (tailles 40 et 30 ).
- `CharField` avec choix pour `patient_genre` afin de restreindre à H/F/A.
- `PositiveSmallIntegerField` pour ne pas accespter les ages négatifs.
- `TextField` pour la description, car le texte peut être long.
- `DateField` pour la date de consultation.
- Aucun champ n’a `null=True` pour respecter la contrainte "aucun champ ne peut recevoir la valeur null".
- pour le shell on a creer 4 consultations.
## Question 4
### Commandes utilisées:
- python manage.py dumpdata medico.Consultation --output=medico/fixtures/examples.json:permet d’exporter toutes les données existantes du modèle Consultation vers un fichier JSON qu'on a appelé examples.json
- python manage.py loaddata examples:permet de charger les données contenues dans le fichier examples.json vers la base de données.
- Consultation.objects.count():permet de compter le nombre total de consultations(12)
- Consultation.objects.all():permet d'afficher la liste de toutes les consultations présentes dans la base de données.  

## Question 5
- Création d’une vue et d’un template permettant d’afficher les détails d’une consultation à partir de son identifiant

## Question 6
- Vue et template ajoutés pour afficher la liste tabulaire des consultations avec les informations essentielles et un lien vers la fiche détaillée

## Question 7
- vue et le template associé pour permettre l’ajout d’une nouvelle consultation. 
- Ajout de la vue `nouvelle_consultation` 
- Ajout de l’URL `/nouvelle_consultation/` 
- Création du template `nouvelle_consultation.html`
- La date de consultation est automatiquement générée avec `timezone.now()`

## Question 8
- vue et le template associé pour permettre de supprimer une consultation. 
- Ajout de la vue `consultation_confirm_delete` 
- Ajout de l’URL `/effacer_consultation/` 
- Création du template `consultation_confirm_delete.html`

## Question 9
Création d’une vue et d’un template permettant de modifier une consultation existante via un formulaire pré-rempli (instance), sans changer la date, accessible à l’URL /changer_consultation/<id>/.

## Question 10
- Création du template  pour une page principale avec intégration de Bootstrap
  (navbar, container, etc.).
- L’URL d’accès a la racine
- Amélioration de l’esthétique des pages grâce à Bootstrap

## Question 11

### Objectif
Création du modèle Traitement pour gérer les traitements associés à une consultation.

### Modifications effectuées
- Ajout de la classe Traitement dans medico/models.py avec les champs :
  - medicament : nom du médicament
  - quantite : quantité prescrite
  - contenant : forme du conditionnement (boîte, bouteille, etc.)
  - duree : durée du traitement en jours
  - frequence : fréquence de prise (ex: 3 fois par jour)
  - posologie : moment de la prise (ex: matin et soir)
  - consultation : clé étrangère vers le modèle Consultation
- Relation : une consultation peut avoir plusieurs traitements. Un traitement n’est associé qu’à une seule consultation.
- Exécution des commandes :
  python manage.py makemigrations medico
  python manage.py migrate

  ## Question 12
Création des vues et templates nécessaires Permettre d’ajouter, consulter, modifier et supprimer les traitements associés à une consultation.

### Modifications réalisées
- Création d’un `TraitementForm` dans `medico/forms.py` 
- Ajout des vues suivantes dans `medico/views.py` :
  - `ajouter_traitement(consultation_id)` : création d’un traitement pour une consultation donnée.
  - `modifier_traitement(pk)` : modification d’un traitement existant.
  - `supprimer_traitement(pk)` : suppression d’un traitement existant avec page de confirmation.
- Mise à jour du template `consultation_detail.html` pour afficher la liste des traitements associés
  à une consultation et proposer des liens pour ajouter, modifier et supprimer un traitement.
- Création des templates :
  - `traitement_form.html` pour l’ajout et la modification des traitements.
  - `traitement_confirm_delete.html` pour la confirmation de suppression.


## Question 13 – Extensions de l’application Medico

Nous avons conçu plusieurs extensions autour de l’application de base (gestion de consultations et de traitements) afin de la rendre plus proche d’un véritable outil utilisé par un médecin au quotidien.


### 1. Génération d’une ordonnance médicale imprimable

**Objectif :**  
Permettre au médecin d’éditer rapidement une ordonnance lisible et imprimable à partir d’une consultation existante, avec les traitements associés.

**Fonctionnalités :**

- Depuis la page de détail d’une consultation, un lien permet d’accéder à une page d’**ordonnance**.
- L’ordonnance contient :
  - les informations du cabinet 
  - les informations du patient
  - la date et le numéro de consultation,
  - la liste des traitements prescrits (médicament, quantité, durée, posologie),
  - un bloc “Fait à Orléans, le …” et “Signature du médecin”.
- Un bouton **“Imprimer l’ordonnance”** et une feuille de style spéciale **cache le menu et le footer** pour l’impression (ordonnance propre type A4).


### 2. Historique de patient avec tendance de l’état de santé

**Objectif :**  
Donner au médecin une vision globale de l’évolution de l’état d’un patient à travers ses consultations.

**Fonctionnalités :**

- Nouveau menu **“Patients”** dans la barre de navigation qui mène à `/patients/`.
- Page `/patients/` :
  - affiche la liste des patients distincts 
  - affiche le **nombre de consultations** par patient,
  - propose un bouton “Voir l’historique” pour accéder à la page du patient.
- Page d’**historique d’un patient**  :
  - liste toutes les consultations de ce patient (du plus récent au plus ancien),
  - pour chaque consultation : date, extrait de description, , nombre de traitements, lien vers le détail.
  - calcule une **tendance de l’état du patient** sur les 3 dernières consultations :


### 3. Graphique d’évolution des consultations d’un patient

**Objectif :**  
Enrichir l’historique du patient avec un **graphique** représentant le nombre de consultations au fil du temps.

**Fonctionnalités :**

- Sur la page d’historique d’un patient, un bloc “Évolution du nombre de consultations” affiche un **graphique en ligne**.
- Le graphique montre le **nombre de consultations par mois** pour ce patient.
- Si les données sont insuffisantes, un message s’affiche à la place (“Pas encore assez de données pour afficher un graphique”).


### 4. Assistant vocal du médecin pour la description de consultation

**Objectif :**  
Permettre au médecin de **dicter la description** d’une consultation à la voix, pour gagner du temps et améliorer le confort d’utilisation.

**Fonctionnalités :**

- Sur les pages de **création** et de **modification** d’une consultation :
  - ajout d’un bouton avec un **micro** (“Dicter la description”),
  - quand le médecin clique sur le micro, la dictée vocale commence,
  - le texte reconnu est automatiquement ajouté dans le champ `description`.
- La dictée utilise la langue française (`fr-FR`).

### 5. Extension de la satisfaction du médecin (conçue)

**Objectif :**  
Permettre au médecin d’attribuer une **note de satisfaction** à chaque consultation et de disposer d’une vue globale de cette satisfaction.

**Idée fonctionnelle :**

- Ajout d’un champ `satisfaction` (valeur entière de 1 à 5) dans le modèle `Consultation`.
- Dans la vue de détail, affichage de la note sous forme d’étoiles ou de badge (ex. 3/5).
- Page dédiée `/stats_satisfaction/` :
  - moyenne globale des notes de satisfaction,
  - répartition des notes (combien de consultations à 1, 2, 3, 4, 5).


### 6. Filtrer les consultations par date 

**Objectif :**  
Faciliter l’analyse et la recherche de consultations en permettant de **filtrer par intervalle de dates**.

**Idée fonctionnelle :**

  - ajout d’un petit formulaire avec deux champs : **date de début** et **date de fin**,
  - affichage uniquement des consultations comprises dans cet intervalle.


### 7. Gestion des rendez-vous 

**Objectif :**  
Ajouter au logiciel une **gestion de l’agenda** du médecin, en plus des consultations déjà réalisées.

**Idée fonctionnelle :**

- Nouveau modèle `RendezVous` contenant :
  - nom du patient,
  - date et heure du rendez-vous,
  - raison de la consultation,
  - statut (à venir, terminé, annulé).
- Fonctionnalités prévues :
  - ajout d’un rendez-vous,
  - modification,
  - suppression,
  - affichage sous forme de liste ou d’agenda.

