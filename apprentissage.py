# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 11:23:24 2015

@author: 3301031
"""
import numpy as np
import pickle
import os
import classes

# list_fun_features=[distance_ball,distance_mon_but,distance_autre_but,distance_ball_mon_but,distance_ball_autre_but]

def gen_feature_simple(state,teamid,playerid):
    player=state.get_player(teamid,playerid)
    l=[classes.estDansCages(state, player, teamid), classes.balleProche(state, player), classes.teamAdverse(teamid), classes.cagesAdverse(teamid), classes.joueurAdverseProche(state, teamid, player), classes.joueurAdversaireDerriere(state, teamid, player, adv), classes.centreSurface(state, teamid, player), classes.dansSurface(state, teamid, position), classes.dansTerrain(state, teamid, position), classes.distAdv(state, teamid, player), classes.quiABalle(state, teamid, player)]
    return np.array(l)
    
