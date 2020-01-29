#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 14:51:28 2018

@author: Laura Dupuis, Pierre Laffitte et Charlène Noé
"""

from bokeh.plotting import figure
from bokeh.models import HoverTool

### HoverTool : outils pour les graphs
tools = 'xbox_select,reset'

# Commentaires pour panel 1, graph du haut
hover_plot1 = HoverTool(
    tooltips= [
        ("Date", "@date_formatted"),
        ("Hour", "@hour_formatted"),
        ("Price","@price{0.01€}"),
        ],
    mode='vline'
)

# Commentaires pour panel 2, graph de droite
hover_plot2 = HoverTool(
    line_policy='next',
    tooltips=[
        ("Name","@legend"),
        ("Hour","$x{0}"),
        ("Price","$y{0.01€}"),
    ],
)

### Création des plots

# Création du graphique dynamique pour le panel 1
def make_plot_dyn(source,title):
    plot_dyn = figure(plot_width=1200,height=350,x_axis_type='datetime',tools='pan,wheel_zoom,reset')
    plot_dyn.line(x='date',y='price',source=source)
    
    # fixed attributes
    plot_dyn.xaxis.axis_label = None
    plot_dyn.yaxis.axis_label = "Price (€)"
    plot_dyn.axis.axis_label_text_font_style = "bold"
    plot_dyn.grid.grid_line_alpha = 0.3
    plot_dyn.title.text = title
    # hovertools
    plot_dyn.add_tools(hover_plot1)
    
    return plot_dyn

# Création du graphique statique pour le panel 1 (celui de la sélection)
def make_plot_complet(source):
    plot_complet = figure(plot_width=1200, height=170,tools=tools,x_axis_type='datetime', active_drag="xbox_select")
    plot_complet.line(x='date', y='price', source=source)
    plot_complet.circle_x(x='date', y='price', size=0.5, color=None, source=source, selection_color="orange",
                          alpha=0.8, nonselection_alpha=0, selection_alpha=0.4)
    
     # fixed attributes
    plot_complet.xaxis.axis_label = None
    plot_complet.yaxis.axis_label = "Price (€)"
    plot_complet.axis.axis_label_text_font_style = "bold"
    plot_complet.grid.grid_line_alpha = 0.3
    plot_complet.title.text = "Select a range on this graph"
    
    return plot_complet

# Création du graphique du clustering pour le panel 2 (à gauche)
def make_plot_daily_profile_month(source1, source2, title):
    # Initialisation du plot
    plot_dpm = figure(width=900, height=500)
    plot_dpm.title.text = title
    plot_dpm.x_range.start = 0
    plot_dpm.x_range.end = 23
    plot_dpm.xaxis.axis_label = "Hour (h)"
    plot_dpm.yaxis.axis_label = "Price (€)"
    plot_dpm.axis.axis_label_text_font_style = "bold"
    plot_dpm.grid.grid_line_alpha = 0.3

    # Multilignes  
    plot_dpm.multi_line(xs='xs', ys='ys', line_width=2, color='colors', source=source1)
    plot_dpm.multi_line(xs='xs', ys='ys', line_width=2, color='colors', legend = 'legend', line_dash = "dashed", source=source2)
    # Emplacement de la légende
    plot_dpm.legend.location = "top_left"
    
    return plot_dpm

# Création du graphique des détails du clustering pour le panel 2 (à droite)
def make_plot_details(source, title):
    # Initialisation du plot
    plot_details = figure(width=800, height=500)
    plot_details.title.text = title
    plot_details.x_range.start = 0
    plot_details.x_range.end = 23
    plot_details.xaxis.axis_label = "Hour (h)"
    plot_details.yaxis.axis_label = "Price (€)"
    plot_details.axis.axis_label_text_font_style = "bold"
    plot_details.grid.grid_line_alpha = 0.3

    # Multilignes
    plot_details.multi_line(xs='xs', ys='ys', color='color', legend='legend', line_width=2, source=source)
    # Hovertool
    plot_details.add_tools(hover_plot2)
    # Emplacement de la légende
    plot_details.legend.location = "top_left"
    
    return plot_details
    
    