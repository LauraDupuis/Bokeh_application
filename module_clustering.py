#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 14:53:57 2018

@author: Laura Dupuis, Pierre Laffitte et Charlène Noé
"""
import random
from math import sqrt

### Code clustering sur la distance DTW

# Calcul de la distance euclidienne entre deux séries temporelles
def euclid_dist(t1,t2,w):
    return sqrt(sum((t1-t2)**2))

# Calcul de la distance DTW entre deux séries temporelles
def DTWDistance(s1, s2,w):
    DTW={}

    w = max(w, abs(len(s1)-len(s2)))
    
    for i in range(-1,len(s1)):
        for j in range(-1,len(s2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0
  
    for i in range(len(s1)):
        for j in range(max(0, i-w), min(len(s2), i+w)):
            dist= (s1[i]-s2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])
		
    return sqrt(DTW[len(s1)-1, len(s2)-1])

# Applique algorithme de Keogh entre deux séries temporelles
def LB_Keogh(s1,s2,r):
    LB_sum=0
    for ind,i in enumerate(s1):
        
        lower_bound=min(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
        upper_bound=max(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
        
        if i>upper_bound:
            LB_sum=LB_sum+(i-upper_bound)**2
        elif i<lower_bound:
            LB_sum=LB_sum+(i-lower_bound)**2
    
    return sqrt(LB_sum)

# Clustering sur un dataframe avec un nombre d'itérations défini
def k_means_clust(data,num_clust,num_iter,w,metric):
    centroids=random.sample(list(data),num_clust)
    counter=0
    # Pour chaque itération
    for n in range(num_iter):
        counter+=1
        print(counter)
        assignments={}
        # On assigne les données à un cluster
        for ind,i in enumerate(data):
            min_dist=float('inf')
            closest_clust=None
            for c_ind,j in enumerate(centroids):
                if LB_Keogh(i,j,5)<min_dist:
                    cur_dist=metric(i,j,w)
                    #cur_dist=DTWDistance(i,j,w)
                    #cur_dist=euclid_dist(i,j)
                    if cur_dist<min_dist:
                        min_dist=cur_dist
                        closest_clust=c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust]=[]
        
        # On trie par les clés --> new_ass
        kl = [key for key in assignments.keys() if key != None]
        new_kl = sorted(kl)
        new_ass={}
        for key in new_kl:
            new_ass[key] = assignments[key]
        
        # Recalcule les centroîds des clusters -> moyennes
        for key in new_ass:
            clust_sum=0
            for k in new_ass[key]:
                clust_sum=clust_sum+data[k]
            centroids[key]=[m/len(assignments[key]) for m in clust_sum]
        
    return (new_ass,centroids)

# Selon le choix de la métrique, on applique le kmeans
def k_means_clust_metric(data,num_clust,num_iter,w,metric):
    if(metric=="DTW"):
        return k_means_clust(data,num_clust,num_iter,w,DTWDistance)
    if(metric=="Euclidian"):
        return k_means_clust(data,num_clust,num_iter,w,euclid_dist)
    