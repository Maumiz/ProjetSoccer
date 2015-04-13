# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:06:24 2015

@author: 3301031
"""
from soccersimulator import pyglet
from soccersimulator import PygletObserver
from soccersimulator import SoccerBattle, SoccerTeam, SoccerPlayer
from stratsimples import *
from apprentissage import *
from soccersimulator import TreeStrategy
from classes import Attaquant

# équipe pas intelligente
team1=SoccerTeam("Mau F.C")
team1.add_player(SoccerPlayer("t1j1",JoueurFonceur()))


# Apprentissage (équipes intelligentes)
team_tree = SoccerTeam("Team Tree") # création équipe intelligente

treeia=TreeIA(gen_feature_simple,dict({"immobile": Immobile(), "allerverscages": AllerVersCages(), "random": RandomStrategy(),"fonceur": JoueurFonceur(),\
 "allerversballe": AllerVersBalle(), "haut": Haut(), "bas": Bas(), "gauche": Gauche(), "droit": Droit(), "allertirerbas": AllerTirerBas(),\
 "allertirerhaut": AllerTirerHaut(), "allertirercages": AllerTirerCages(), "allerdef": AllerDef()})) # strats nécessaire pour mon défenseur intelligent
 
fn=os.path.join(os.path.dirname(os.path.realpath(__file__)),"Defenseur1.pkl")
treeia.load(fn)

TreeST=TreeStrategy("Defenseur1",treeia)
team_tree.add_player(SoccerPlayer("jintel1", TreeST))

teams = [team1, team_tree]


# Lancement match
battle=SoccerBattle(team1,team_tree)
obs=PygletObserver()
obs.set_soccer_battle(battle)
pyglet.app.run()
