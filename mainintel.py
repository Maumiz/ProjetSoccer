# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:25:18 2015

@author: 3301031
"""

from soccersimulator import pyglet
from soccersimulator import PygletObserver
from soccersimulator import SoccerPlayer, SoccerTeam, InteractStrategy, TreeStrategy
from apprentissage import *
from apprentissage import gen_feature_simple
from stratsimples import * 


# Liste des touches associées à chaque strat pour controler le joueur intelligent
list_key_player1=['w', 'x', 'e', 'r', 't']
list_strat_player1=[AllerDef(), Immobile(), AllerTirerBas(), AllerTirerHaut(), AllerTirerCages()]
inter_strat_player1=InteractStrategy(list_key_player1,list_strat_player1,"Defenseur1")

# création d'une équipe normale et d'une équipe intelligente
team1 = SoccerTeam("Argentina")
team3 = SoccerTeam("MauFc")
team3.add_player(SoccerPlayer("Intel1",inter_strat_player1))
team1.add_player(SoccerPlayer("t1j1",JoueurFonceur()))


battle=SoccerBattle(team1,team3)
obs=PygletObserver()
obs.set_soccer_battle(battle)
pyglet.app.run()

#dot: definition de l'arbre