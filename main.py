1# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 11:34:52 2015

@author:   3301031
"""

from soccersimulator import pyglet
from soccersimulator import PygletObserver
from soccersimulator import SoccerBattle, SoccerTeam, SoccerPlayer
from soccersimulator import *
from classes import *
from apprentissage import *

team1=SoccerTeam("team1")
team2=SoccerTeam("team2")

team1.add_player(SoccerPlayer("t1j1",TreeST()))
team2.add_player(SoccerPlayer("t2j1",Goal1()))
team1.add_player(SoccerPlayer("t1j2",RandomStrategy()))
team2.add_player(SoccerPlayer("t2j2",RandomStrategy()))


battle=SoccerBattle(team1,team2)
obs=PygletObserver()
obs.set_soccer_battle(battle)
pyglet.app.run()



