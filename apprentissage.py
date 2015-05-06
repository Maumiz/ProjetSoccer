# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 11:23:24 2015

@author: 3301031
"""
import numpy as np
import pickle
import os
import stratsimples
from soccersimulator import TreeIA
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH, GAME_GOAL_HEIGHT


# création du générateur de features
def gen_feature_simple(state,teamid,playerid):
    player=state.get_player(teamid,playerid)
    adv = stratsimples.joueurAdverseProche(state,teamid,player)
    l = [
    stratsimples.distAdv(state,teamid,player), int(stratsimples.dansTerrain(state,teamid)),\
    int(stratsimples.dansSurface(state,teamid)),\
    stratsimples.distballon(state, player),stratsimples.distAdvBall(state,teamid,player),\
    int(stratsimples.balleProche(state, player)), stratsimples.distSurface(state, teamid, player),
    ]
    return np.array(l)
    
# fonctions nécessaires pour créer l'arbre 
    
def app():
    treeia=TreeIA(gen_feature_simple)
    treeia.learn(fn="Defenseur1",depth=10)
    treeia.save("Defenseur1.pkl")
    treeia.to_dot("Defenseur1.dot")

if __name__=="__main__":
    app()

# dot -Tpdf nom -o nom.pdf : commande nécessaire pour génerer le pdf d'un arbre

# int(stratsimples.quiBalle(state,teamid,player)), int(stratsimples.estDansCages(state,teamid,player))