# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 19:32:52 2015

@author: 3301031
"""


from soccersimulator import SoccerBattle, SoccerTeam, SoccerPlayer
from classes import *

team1=SoccerTeam("BocaJuniors")
team2=SoccerTeam("team2")
BocaJuniors.add_player(SoccerPlayer("t1j1",JoueurFonceur()))
BocaJuniors.add_player(SoccerPlayer("t1j2",RandomStrategy()))
team2.add_player(SoccerPlayer("t2j1",ComposeStrategy(DefenseurContreAttaque(), JoueurFonceur())))
team2.add_player(SoccerPlayer("t2j2",RandomStrategy()))
team2.add_player(SoccerPlayer("t2j3",GoalContreAttaque()))
team2.add_player(SoccerPlayer("t2j3",DefenseurContreAttaque()))

teams = [team1, team2]
names = "MAUFC"
