#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:05:19 2018

@author: Laura Dupuis, Pierre Laffitte et Charlène Noé
"""
from bokeh.models import ColumnDataSource
from module_selection import data_nb_individuals, apply_kmeans
import numpy as np
from bokeh.palettes import brewer

### Fonctions de transformations

# Transformation en ColumnDataSource du dataframe pour le plot dynamique du panel 1
def get_data_country(data_c):
    source = ColumnDataSource(data=dict(date=[], price=[], date_formatted=[], hour_formatted=[]))
    source.data = source.from_df(data_c[['date','price','date_formatted','hour_formatted']])
    
    return source

# Transformation en ColumnDataSource du dataframe pour le plot du clustering du panel 2
def get_data_daily_profile_year(data_dpm, nbCluster, metric, choice_user):
    # Application du kmeans
    data_kmeans = apply_kmeans(data_dpm, nbCluster, metric, choice_user)
    # Récupère les centroids, les couleurs et les clusters générés par le kmeans
    centroids = data_kmeans[0]
    colors = data_kmeans[1]
    clusters = data_kmeans[2]
    # Ajoute les centroïds au dataframe initial
    i = 0
    for cluster in centroids:
        data_dpm["cluster" + (str(i+1))] = centroids[i]
        i = i +1
            
    # Transforme en dictionnaire
    nb_columns = data_dpm.shape[1]
    xs_list = [data_dpm.index.values]*nb_columns
    ys_list = [data_dpm[name].values for name in data_dpm]
    legend = [name for name in data_dpm]
    # Caste en columndatasource : source1 = clusters et source2 = centroîds
    col1 = nb_columns - int(nbCluster)
    source1 = ColumnDataSource(data=dict(xs=xs_list[0:col1], ys=ys_list[0:col1], legend=legend[0:col1], colors=colors[0:col1]))
    source2 = ColumnDataSource(data=dict(xs=xs_list[col1:nb_columns], ys=ys_list[col1:nb_columns], legend=legend[col1:nb_columns], colors=colors[col1:nb_columns]))
    
    return (source1,source2,clusters)

# Transformation en ColumnDataSource du dataframe pour le plot des détails du clustering du panel 2
def get_details(data_dpm, clusters, selected_cluster, nb_ind):
    # Récupère l'échantillonnage pour le graphique : [0] = prix et [1] = dates
    sel_clust = data_nb_individuals(data_dpm, clusters, selected_cluster, nb_ind)
    # Si pas assez d'individus
    if(int(nb_ind) > len(sel_clust[1])):
        nb_ind = len(sel_clust[1])
    # Transforme en dictionnaires : échantillons
    xs_list_clust = [np.arange(24)]*int(nb_ind)
    ys_list_clust = sel_clust[0]
    legend_clust = sel_clust[1]
    color = brewer['Paired'][int(nb_ind)]
    # Caste en ColumnDataSource
    source = ColumnDataSource(data=dict(xs=xs_list_clust,ys=ys_list_clust,legend=legend_clust,color=color))
    
    return source