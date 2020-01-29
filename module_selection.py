#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 14:48:31 2018

@author: Laura Dupuis, Pierre Laffitte et Charlène Noé
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime
from module_clustering import k_means_clust_metric
from module_transfData import transform_data_before_clust

### Index des pays et des couleurs
COUNTRIES_INDEX = {"Germany":"DE","France":"FR","Netherlands":"NL","Belgium":"BE","Portugal":"PT"}
COLORS_INDEX = {"0" : "beige", "1" : "darkorange", "11" : "peachpuff", 
                "2" : "red", "22" : "lightpink", "3" : "darkblue",
                "33" : "lightblue", "4" : "green", "44" : "lightgreen",
                "5" : "darkviolet", "55" : "thistle"}

### Fonctions de sélection

# Dataframe contenant l'ensemble des prix pour un pays donné
def select_country(data_init,country):
    tmp = data_init[(data_init.country == COUNTRIES_INDEX[country])]
    tmp.index = range(1, tmp.shape[0]+1)
    tmp = tmp.loc[:,['newDate','Price']]
    tmp['newDate'] = pd.to_datetime(tmp['newDate'])
    tmp['date_formatted'] = [e.strftime('%Y-%m-%d') for e in tmp['newDate']]
    tmp['hour_formatted'] = [e.strftime('%H:00:00') for e in tmp['newDate']]
    data = pd.DataFrame({'date': tmp.newDate, 'price': tmp.Price, 'date_formatted' : tmp.date_formatted, 'hour_formatted': tmp.hour_formatted})   
    
    return data

# Dataframe contenant les prix pour un jour donné : index = les heures / 1 colonne = price
def select_day(data_init, day):
    d = datetime.strptime(day, '%Y-%m-%d')
    day_string = d.strftime('%Y-%m-%d')
    tmp = data_init[(data_init.Date >= day_string) & (data_init.Date <= day_string)]
    tmp.index = tmp.Hour_Start
    data = tmp.loc[:,'Price']
    
    return data

# Gestion de la date
class Date:
    def __init__(self, annee, mois, jour):
        self.year = annee
        self.month = mois
        self.day = jour
        
# Gestion type de date
def type_date(value_widget):
    if value_widget=="All":
        return ['monday','tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday']
    if value_widget=="WeekDay":
        return ['monday','tuesday', 'wednesday', 'thursday', 'friday']
    if value_widget=="WeekEnd":
        return ['saturday','sunday']
    
# Dataframe contenant les prix pour un pays et une plage donnée
def select_plage(data_init, debut, fin, country, value_widget_date):
    # Sélection de la plage
    tmp = data_init[(data_init.year >= debut.year) & (data_init.year <= fin.year) & (data_init.country == COUNTRIES_INDEX[country])]
    tmp = tmp[ ~((tmp.year == debut.year ) & (tmp.month < debut.month))]
    tmp = tmp[~((tmp.year == debut.year) & (tmp.month == debut.month) & (tmp.day < debut.day))]
    tmp = tmp[ ~((tmp.year == fin.year ) & (tmp.month > fin.month))]
    tmp = tmp[~((tmp.year == fin.year) & (tmp.month == fin.month) & (tmp.day > fin.day))]
    tmp=tmp[tmp.day_of_week.isin(type_date(value_widget_date))]
    tmp.index = range(1, tmp.shape[0]+1)
    tmp = tmp.loc[:,['Date','Hour_Start','Price']]
    # Récupère les jours
    list_days = list(dict.fromkeys(tmp.Date.str.slice(0,10)))
    # Création dataframe contenant profil journalier pour chaque jour
    tmp2 = pd.DataFrame(index=range(0,24),columns=list_days)
    for day in list_days:
        df = select_day(tmp,day)
        tmp2[day] = df
        
    return tmp2

# Transforme le dataframe des données pour le clustering : 
# Renvoie un tuple avec un dictionnaire associé l'indice du jour à sa date : indices={indice : 'date'} 
# et un np.array de liste des prix associé à chaque jour
def transform_data_for_clustering(data_dpm):
    df_array = []
    indices = {}
    i=0
    # Pour toutes les dates du dataframe
    for name in data_dpm.columns:
        indices[i] = name # indices[indice] = 'date'
        tmp = list(data_dpm[name]) # liste des prix associé à cette date
        df_array.append(tmp) # ajoute à la liste
        i = i+1
    # Transformation en np.array de la liste des prix
    df_array = np.array(df_array)
    
    return (indices,df_array)

# Application du kmeans sur un dataframe avec un nombre de clusters choisi
def apply_kmeans(data_dpm, nbCluster, metric, choice_user):
    # Transformation ou pas ?
    data_tr = transform_data_before_clust(data_dpm,choice_user)
    # Transformation du dataframe : dict(indices) et np.array(prix)
    data_transform = transform_data_for_clustering(data_tr)
    # Applique les kmeans avec 10 itérations
    kmeans = k_means_clust_metric(data_transform[1],int(nbCluster),10,4,metric)
    # Récupère les détails (ie. indices) des groupes
    clusters = kmeans[0]
    # Récupère centroïds : si pas de transformation = centroids de la transformation
    # si transformation : centroids des séries initiales
    if(choice_user=="None"):
        centroids = kmeans[1]
    else:
        centroids = compute_centroids(data_dpm,clusters)
        
    # Initialisation des couleurs : 0 = pas d'affection
    colors=["0"]*data_transform[1].shape[0]
    # Affectation des couleurs pour chaque clusters 
    for key in clusters.keys():
        if key != None:
            for i in clusters[key]:
                colors[i] = str(key+1) *2 # on double le numéro du cluster pour les couleurs pastels
    # Ajoute les couleurs pour les centroïds : couleurs brutes (1 numéro)
    for i in range(0,int(nbCluster)):
        colors = colors + [str(i+1)]
    # Liste des couleurs finales : transformation des 0,1,2.. en couleurs
    colors = [ COLORS_INDEX[c] for c in colors ] 
    
    return (centroids,colors,clusters)

# Echantillonnage du cluster choisi : renvoie liste de np.array(prix) et liste des 'dates'
def data_nb_individuals(data_dpm, clusters, nb_clust, nb_ind):
    # Transformation du dataframe : dict(indices) et np.array(prix)
    data_transform = transform_data_for_clustering(data_dpm)
    # Liste des indices des dates selon le cluster choisi
    cluster_choose = clusters[int(nb_clust)-1]
    # Si le cluster est très spécifique (ie. nb ind petit)
    if(len(cluster_choose) < int(nb_ind)):
        nb_ind = len(cluster_choose)
    # Echantillonnage sur les indices du cluster choisi
    ind_plot = random.sample(cluster_choose, int(nb_ind))
    
    # Echantillon : valeurs (cluster_to_plot) et dates (name_to_plot)
    cluster_to_plot = [np.array(i) for i in data_transform[1][ind_plot]]
    name = data_transform[0]
    name_to_plot = [name[i] for i in ind_plot]
    
    return (cluster_to_plot,name_to_plot)

# Recalcule centroids
def compute_centroids(data_dpm,clusters):
    centroids = []
    for num_cluster in clusters.keys():
        clust_sum = 0
        for value in clusters[num_cluster]:
            clust_sum = clust_sum + data_dpm.iloc[:,value]
        centroids.append([m/len(clusters[int(num_cluster)]) for m in clust_sum])
    return centroids
