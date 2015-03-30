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
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH, GAME_GOAL_HEIGHT


# création du générateur de features
def gen_feature_simple(state,teamid,playerid):
    player=state.get_player(teamid,playerid)
    adv = classes.joueurAdverseProche(state,teamid,player)
    
    l=[int(classes.quiBalle(state,teamid,player)), classes.distAdv(state,teamid,player), int(classes.dansTerrain(state,teamid)),\
    int(classes.dansSurface(state,teamid)), classes.centreSurface(state,teamid,player), int(classes.JoueurAdverseDerriere(state,teamid,player,adv)),\
    classes.joueurAdverseProche(state,teamid,player), int(classes.balleProche(state,player)), int(classes.estDansCages(state,teamid,player)),\
    classes.distBallon(state,player), classes.distAdvBall(state,teamid,player), int(classes.estDansCages(state, teamid, player)), int(classes.balleProche(state, player))]
    # fonctions nécessaires pour créer l'arbre 
    
    return np.array(l)
    
    
def app():
    treeia=TreeIA(gen_feature_simple)
    treeia.learn(fn="Defenseur1",depth=10)
    treeia.save("Defenseur1.pkl")
    treeia.to_dot("Defenseur1.dot")

#app()
# dot -Tpdf nom -o nom.pdf : commande nécessaire pour génerer le pdf d'un arbre
