#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 14:07:47 2018

@author: Laura Dupuis, Pierre Laffitte et Charlène Noé
"""

from datetime import datetime
import pandas as pd
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs, Panel
from bokeh.layouts import column,row

# Modules
from module_transformation import get_data_country, get_data_daily_profile_year, get_details
from module_plot import make_plot_complet, make_plot_daily_profile_month, make_plot_dyn, make_plot_details
from module_selection import select_country, select_plage, Date
from module_widget import widget_country, widget_country_2, widget_nb_clusters, widget_start, widget_end, widget_selected_nbInd
from module_widget import widget_selected_cluster, div_part1, div_part2, div_part2_2, widget_type_date, widget_metric, widget_transformation
from module_widget import country, nbCluster, nb_ind, selected_cluster, type_date, metric_init, transf_init

### Données initiales
data_load = pd.read_csv("./data_cleanv2.csv", header=0)
start_date = Date(2013,1,1)
end_date = Date(2013,12,31)

########################################################################################################################
########################################################################################################################

### Update

# Mise à jour du graphique quand le pays change (panel 1)
def update_plot_country(attrname,old,new):
    # Récupère le pays choisi
    c = widget_country.value
    # Mise à jour du titre
    plot_dyn.title.text = 'Price for %s' % (c)
    # Mise à jour des sources de données selon les choix faits
    data = get_data_country(select_country(data_load,c))
    src.data = data.data
    src_static.data = data.data

# Mise à jour du graphique quand on fait une sélection (panel 1)
def update_selection_on_graph(attrname,old,new):
    # Récupère les indices de la sélection
    selected = src_static.selected['1d']['indices']
    # Si il y a une sélection
    if(selected):
        # Récupère data pour un pays puis seulement la sélection
        data_country = select_country(data_load,country) 
        data_country = data_country.iloc[selected, :].sort_values(by = 'date')
        # On modifie la source
        src.data = get_data_country(data_country).data
    # Si pas de sélection
    else:
       src.data = src_static.data

# Mise à jour des graphiques du clustering (panel 2)
def update_plot_clustering(attrname,old,new):
    # Graphique 1
    # Récupère les différentes valeurs des widgets
    clusters = widget_nb_clusters.value
    c = widget_country_2.value
    start = widget_start.value
    end = widget_end.value
    date = widget_type_date.value
    metric = widget_metric.value
    transf = widget_transformation.value
    # Mise à jour du titre
    plot_dpm.title.text = "Daily profiles from %s to %s in %s"% (datetime(start.year,start.month,start.day).strftime('%Y-%m-%d'), 
                                                                datetime(end.year,end.month,end.day).strftime('%Y-%m-%d'), c)
    # Mise à jour des sources de données selon les choix faits
    data = select_plage(data_load,Date(start.year,start.month,start.day),Date(end.year,end.month,end.day),c,date)
    # Mise à jour des sources (ColumnDataSource)
    src = get_data_daily_profile_year(data,clusters,metric,transf)
    src_dpm.data = src[0].data
    src_dpm_kmeans.data = src[1].data
    
    # Change les variables globales : clusters et data_dpm
    global src_2, data_dpm
    tupl = list(src_2)
    tupl[2] = src[2]
    src_2 = tuple(tupl)
    data_dpm = data
    
    # Graphique 2
    # On instancie à 1 pour éviter les erreurs (avant : 4 clusters -> choisi cluster 4 -> nouveau kmeans avec 3 clusters)
    widget_selected_cluster.value = "1"
    selected_cluster = widget_selected_cluster.value
    nb_ind = widget_selected_nbInd.value
    # Mise à jour du titre
    plot_details.title.text = "Details for cluster n°%s - %s individuals" % (selected_cluster, nb_ind)
    # Mise à jour source de données pour graphique des détails du clustering
    src_details.data = get_details(data, src[2], selected_cluster, nb_ind).data
    
# Mise à jour du graphique des détails du clustering
def update_plot_det(attrname,old,new):
    # Récupère numéro du cluster et le nombre d'individus dans l'échantillon sélectionnés
    selected_cluster = widget_selected_cluster.value
    nb_ind = widget_selected_nbInd.value
    # Mise à jour du titre
    plot_details.title.text = "Details for cluster n°%s - %s individuals" % (selected_cluster, nb_ind)
    # Variables globales
    global src_2, data_dpm
    # Mise à jour source de données pour graphique des détails du clustering
    src_details.data = get_details(data_dpm, src_2[2], selected_cluster, nb_ind).data

# Mise à jour des options de sélection du widget de sélection de clusters
def update_widget_selected_cluster(attrname,old,new):
    # Instancie à 1
    widget_selected_cluster.value = "1"
    # Récupère le nombre de clusters choisi et on change les options
    nbCluster = widget_nb_clusters.value
    options = [str(i) for i in range(1,int(nbCluster)+1)]
    widget_selected_cluster.options = options

# Mise à jour de la date max du widget start (égale à la date actuelle du widget end)
def update_widget_start(attrname,old,new):
    widget_start.max_date = widget_end.value
    
    
########################################################################################################################
########################################################################################################################

### Sources initiales

# Panel 1
data_country = select_country(data_load,country) 
src = get_data_country(data_country)
src_static = get_data_country(data_country)
# Panel 2
data_dpm = select_plage(data_load,start_date,end_date,country,type_date)
src_2 = get_data_daily_profile_year(data_dpm, nbCluster, metric_init, transf_init)
src_dpm = src_2[0]
src_dpm_kmeans = src_2[1]
src_details = get_details(data_dpm, src_2[2], selected_cluster, nb_ind)

### Plots

# Panel 1
plot_dyn = make_plot_dyn(src, "Price for " + country)
plot_complet = make_plot_complet(src_static)
# Panel 2
plot_dpm = make_plot_daily_profile_month(src_dpm,src_dpm_kmeans, 
                                         "Daily profiles from %s to %s in %s"% (datetime(start_date.year,start_date.month,start_date.day).strftime('%Y-%m-%d'), 
                                                                               datetime(end_date.year,end_date.month,end_date.day).strftime('%Y-%m-%d'), country))
plot_details = make_plot_details(src_details, "Details for cluster n°%s - %s individuals" % (selected_cluster, nb_ind))

### Widgets change

# Panel 1
widget_country.on_change('value', update_plot_country)
# Panel 2
# Plot1 - update widgets
widget_nb_clusters.on_change('value', update_widget_selected_cluster)
widget_end.on_change('value',update_widget_start)
# Plot 2 - update plot clustering
widget_nb_clusters.on_change('value', update_plot_clustering)
widget_start.on_change('value', update_plot_clustering)
widget_end.on_change('value', update_plot_clustering)
widget_country_2.on_change('value',update_plot_clustering)
widget_type_date.on_change('value',update_plot_clustering)
widget_metric.on_change('value',update_plot_clustering)
widget_transformation.on_change('value',update_plot_clustering)
# Plot 2 - update plot details
widget_selected_cluster.on_change('value', update_plot_det)
widget_selected_nbInd.on_change('value', update_plot_det)

### Source change

# Panel 1
src_static.on_change('selected',update_selection_on_graph)

### Panel : organisation des widgets et plots sur les pages
controlsPart1 = column(div_part1,row(widget_country))
layoutPart1 = column(controlsPart1, plot_dyn, plot_complet)

controlsPart2 = column(div_part2,row(widget_start,widget_end,widget_country_2),row(widget_nb_clusters,widget_type_date,widget_metric,widget_transformation))
controlsPart_2 = column(div_part2_2,row(widget_selected_cluster, widget_selected_nbInd))

tab1 = Panel(child=layoutPart1, title="Global")
tab2 = Panel(child=column(row(controlsPart2,controlsPart_2),row(plot_dpm,plot_details)), title="Daily profiles")
tabs = Tabs(tabs=[ tab1, tab2 ])

### Affichage de l'application
curdoc().add_root(tabs)
curdoc().title = "Visualization of prices"
