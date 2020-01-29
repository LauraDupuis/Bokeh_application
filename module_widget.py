#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:00:24 2018

@author: charlene
"""
from bokeh.models import Select, Div, DatePicker
from module_selection import COUNTRIES_INDEX
from datetime import datetime

### Valeur par défaut
country = "Belgium"
nbCluster = "3"
selected_cluster = "1"
nb_ind = "4"
type_date="All"
metric_init = "DTW"
transf_init = "None"

### Widgets
# Panel 1
widget_country = Select(title="Country :", value=country, options=sorted(COUNTRIES_INDEX), width=170)
div_part1 = Div(text="""
                <h2> Global visualization </h2>
                Select the country of your choice and the desired range on the bottom graph.""", width=900)

# Panel 2
# Plot 1
widget_country_2 = Select(title="Country", value=country, options=sorted(COUNTRIES_INDEX),width=170)
widget_nb_clusters = Select(title="Number of clusters", value=nbCluster, options=["3","4","5"],width=170)
widget_start = DatePicker(title="Start date", min_date=datetime(2013,1,1),max_date=datetime(2013,12,31),value=datetime(2013,1,1))
widget_end = DatePicker(title="End date", min_date=datetime(2013,1,1),max_date=datetime(2017,4,30),value=datetime(2013,12,31))
widget_type_date = Select(title="Type of date", value=type_date, options=["All","WeekDay","WeekEnd"],width=170)
widget_metric = Select(title="Metric", value=metric_init, options=["DTW","Euclidian"],width=170)
widget_transformation = Select(title="Data transformation", value=transf_init, options=["None","ACF","Fourier","Variance"],width=170)
div_part2 = Div(text="""
                <h2> Visualization of daily profiles on a specific range </h2>
                Select the time range, the country, the number of clusters, the type of date, the metric and the data transformation desired.""", width=900)
# Plot 2
widget_selected_cluster = Select(title="Cluster", value=selected_cluster, options=["1","2","3"],width=170)
widget_selected_nbInd = Select(title="Number of individuals", value=nb_ind, options=["4","6","8"],width=170)
div_part2_2 = Div(text="""
                  <h2><br></h2>
                  Select a cluster and the number of individuals to display its detail.""", width=400)