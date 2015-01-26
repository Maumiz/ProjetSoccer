# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ce script temporaire est sauvegardé ici :
/users/Etu1/3301031/.spyder2/.temp.py
"""
import pyglet
from soccersimulator import Vector2D, SoccerAction, SoccerPlayer , PLAYER_RADIUS, BALL_RADIUS

v=Vector2D(1, 2)
v2=v+Vector2D(3, 4)

u=Vector2D(1, 3)

w=u+v 

w.norm
u.norm

u.norm
u.x

acceleration=Vector2D(1,3)
shoot=Vector2D(10, 10)

action= SoccerAction(acceleration, shoot)

pos = Vector2D.create_random()
shoot = Vector2D.create_random()
action = SoccerAction (pos,shoot)


from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy 
from soccersimulator import PygletObserver,ConsoleListener,LogListener
class RandomStrategy(SoccerStrategy):
    def __init__(self):
        self.name="Random"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        pos = Vector2D.create_random(-1, 1)
        shoot = Vector2D.create_random(-1, 1)
        action = SoccerAction(pos,shoot)
        return action
    def copy(self):
        return RandomStrategy()
    def create_strategy(self):
        return RandomStrategy()
        


class JoueurFonceur(SoccerStrategy):
    def __init__(self):
        self.name="Fonceur"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        pos = state.ball.position-player.position
        shoot = Vector2D(0,0)
        if (PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position)):
            shoot = Vector2D.create_random(-5, 5)
            teamadverse=2
            if teamid==2:
                teamadverse=1    
            state.get_goal_center(teamadverse)
        return SoccerAction(pos,shoot)
    def copy(self):
        return JoueurFonceur()
    def create_strategy(self):
        return JoueurFonceur()
    

team1=SoccerTeam("team1")
team2=SoccerTeam("team2")
team1.add_player(SoccerPlayer("t1j1",JoueurFonceur()))
team2.add_player(SoccerPlayer("t2j1",JoueurFonceur()))
team1.add_player(SoccerPlayer("t1j2",RandomStrategy()))
team2.add_player(SoccerPlayer("t2j2",RandomStrategy()))
battle=SoccerBattle(team1,team2)
obs=PygletObserver()
obs.set_soccer_battle(battle)
pyglet.app.run()



