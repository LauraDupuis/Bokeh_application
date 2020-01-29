# Bokeh_application

Développer un tableau de bord de modélisation des prix de l'électricité
travaille effectuer pour un projet d'étude en équipe de trois personnes

1. Détails de l'application
Le tableau de bord Bokeh est composé de 7 modules python :
- initialisialisation.py : module de lancement de l'application qui permet d'instancier les différents
objets et de mettre à jour les graphiques. Il est le module "central" de l'application.
- module clustering.py : module regroupant les fonctions liées au clustering : distance euclidienne,
DTW et kmeans.
- module plot.py : module instanciant les graphiques de l'application.
- module selection.py : module rassemblant les fonctions de filtrage.
- module transfData.py : module permettant de réaliser des transformées sur les données avant
d'effectuer le clustering : transformée de Fourier, ACF, etc.
- module transformation.py : module convertissant les données filtrées en ColumnDataSource.
- module widget.py : module initialisant les widgets du tableau de bord.


Le jeu de données de utilisé pour développer l'application a la forme suivante : 
pays / date / heure_debut / heure_fin / prix_electricité


2. Lancement de l'application
Ouvrir une console, se placer dans le dossier des modules python et exécuter la commande suivante :
python3 -m bokeh serve -show initialisation.py
