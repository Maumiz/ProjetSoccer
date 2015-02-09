# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 19:32:52 2015

@author: 3301031
"""


from soccersimulator import SoccerBattle, SoccerTeam, SoccerPlayer
from classes import *

team1=SoccerTeam("C.A BocaJuniors 2v2")
team1.add_player(SoccerPlayer("t1j1",JoueurFonceur()))
team1.add_player(SoccerPlayer("t1j2",GoalContreAttaque()))


team2=SoccerTeam("Argentina 4v4")
team2.add_player(SoccerPlayer("t2j1",ComposeStrategy(DefenseurContreAttaque(), JoueurFonceur())))
team2.add_player(SoccerPlayer("t2j2",RandomStrategy()))
team2.add_player(SoccerPlayer("t2j3",GoalContreAttaque()))
team2.add_player(SoccerPlayer("t2j4",DefenseurContreAttaque()))

team3=SoccerTeam("DiegoMaradona 1v1")
team2.add_player(SoccerPlayer("t2j1",ComposeStrategy(GoalContreAttaque(), JoueurFonceur())))



teams = [team1, team2, team3]


