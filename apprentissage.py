# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 11:23:24 2015

@author: 3301031
"""
import numpy as np
import pickle
import os
import classes
from soccersimulator import TreeIA

# list_fun_features=[distance_ball,distance_mon_but,distance_autre_but,distance_ball_mon_but,distance_ball_autre_but]

def gen_feature_simple(state,teamid,playerid):
    player=state.get_player(teamid,playerid)
    l=[classes.estDansCages(state, player, teamid), classes.balleProche(state, player), classes.teamAdverse(teamid)]
    return np.array(l)
    
if __name__=="__main__":
    treeia=TreeIA(gen_feature_simple)
    treeia.learn(fn="Defenseur1")
    treeia.save("Defenseur1.pkl")
    treeia.to_dot("Defenseur1.dot")

   
# Donner nom strats pr ia
# tree a arbre qui stocke les features et strats