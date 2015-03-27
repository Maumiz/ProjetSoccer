# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:06:24 2015

@author: 3301031
"""

from soccersimulator import SoccerBattle, SoccerTeam, SoccerPlayer
from StratsSimples import *
from apprentissage import *
from soccersimulator import TreeStrategy
from classes import *

team1=SoccerTeam("C.A BocaJuniors 2v2")
team1.add_player(SoccerPlayer("t1j1",RandomStrategy()))
team1.add_player(SoccerPlayer("t1j2",RandomStrategy()))


team2=SoccerTeam("Argentina 4v4")
team2.add_player(SoccerPlayer("t2j1",JoueurFonceur()))
team2.add_player(SoccerPlayer("t2j2",RandomStrategy()))
team2.add_player(SoccerPlayer("t2j3",RandomStrategy()))
team2.add_player(SoccerPlayer("t2j4",RandomStrategy()))

team3=SoccerTeam("DiegoMaradona 1v1")
team3.add_player(SoccerPlayer("t2j1",RandomStrategy()))


### Apprentissage
team_tree = SoccerTeam("Team Tree")

treeia=TreeIA(gen_feature_simple,dict({"random":RandomStrategy(),"fonceur":JoueurFonceur(), "allerversballe":AllerVersBalle(), "haut":Haut(), "bas"Bas(), "gauche"Gauche(), "droit"Droit(), "allertirerbas"AllerTirerBas(), "allertirerhaut"AllerTirerHaut(), "allertirercages"AllerTirerCages())}
fn=os.path.join(os.path.dirname(os.path.realpath(__file__)),"Defenseur1")
treeia.load(fn)

TreeST=TreeStrategy("Defenseur1",treeia)
team_tree.add_player(SoccerPlayer("t1j1", TreeST))


teams = [team1, team2, team3, team_tree]

