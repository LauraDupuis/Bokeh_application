#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 16:51:47 2018

@author: Laura Dupuis, Pierre Laffitte et Charlène Noé
"""
import numpy as np
import pandas as pd
import scipy.io.wavfile

### Fonctions de transformations de données

# ACF en chaque point
def acf(x, length=20):
    res = [1]    
    for i in range(1, length):
        tmp = np.corrcoef(x[:-i], x[i:])
        res.append(tmp.item(2))
    return res

# ACF d'une série
def calculACF(day):
    res = acf(day, 20)
    return pd.Series(res)

# Variance mobile 
def variance_mobile(serie, nb_neigbors):
    res = []
    for i in range(0,serie.size):
        debut = max(0, i-nb_neigbors)
        fin = min(i+nb_neigbors, serie.size -1)
        res.append(np.var(serie[debut:fin]))
    return pd.Series(res)

# Transformation de Fourier sur une série
def transfo_fourier(serie):
    return pd.Series(abs(scipy.fft(serie)))

# Variance mobile à deux voisins
def variance_mobile_2(serie):
    return variance_mobile(serie,2)

# Applique une transformation sur les données selon le choix défini    
def transform_data_before(dpm,choice):
    # Récupère les dates
    date = list(dpm.columns.values)
    l = []
    # Pour toutes les séries, on applique la transformation choisie
    for i in range(0,dpm.shape[1]):
        res = pd.DataFrame(choice(dpm.iloc[:,i]),columns=[date[i]])
        l.append(res)
    res = pd.concat(l,ignore_index=False,axis=1)
    return res

# Transforme les données
def transform_data_before_clust(dpm,choice_user):
    if(choice_user=="None"):
        return dpm
    if(choice_user=="ACF"):
        return transform_data_before(dpm,calculACF)
    if(choice_user=="Fourier"):
        return transform_data_before(dpm,transfo_fourier)
    if(choice_user=="Variance"):
        return transform_data_before(dpm,variance_mobile_2)

