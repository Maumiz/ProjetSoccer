# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 19:32:52 2015

@author: 3301031
"""


from soccersimulator import SoccerBattle, SoccerTeam, SoccerPlayer
from classes import *

team1=SoccerTeam("C.A BocaJuniors 2v2")
team1.add_player(SoccerPlayer("t1j1",Dribbleur()))
team1.add_player(SoccerPlayer("t1j2",Dribbleur()))


team2=SoccerTeam("Argentina 4v4")
team2.add_player(SoccerPlayer("t2j1",Attaquant()))
team2.add_player(SoccerPlayer("t2j2",Goal()))
team2.add_player(SoccerPlayer("t2j3",Intercepteur()))
team2.add_player(SoccerPlayer("t2j4",Intercepteur()))

team3=SoccerTeam("DiegoMaradona 1v1")
team3.add_player(SoccerPlayer("t2j1",ComposeStrategy(GoalContreAttaque(), JoueurFonceur())))



teams = [team1, team2, team3]


