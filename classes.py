# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:58:42 2015

@author: 3301031
"""

from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH 
from soccersimulator import PygletObserver,ConsoleListener,LogListener


def teamAdverse(teamid):
    adv=2
    if (teamid==2):
        adv=1
    return adv




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
            teamadverse=2
            if teamid==2:
                teamadverse=1    
            shoot= (state.get_goal_center(teamadverse)-player.position)
            
        return SoccerAction(pos,shoot)
    def copy(self):
        return JoueurFonceur()
    def create_strategy(self):
        return JoueurFonceur()
        
        
class AllerVersPoint(SoccerStrategy):
    def __init__(self, destination):
        self.name="allerverspoint"
        self.destination=destination
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        deplacement = self.destination - player.position
        shoot = Vector2D(0,0)
        
        return SoccerAction(deplacement,shoot)
    def copy(self):
        return AllerVersPoint(self.destination)
    def create_strategy(self):
        return AllerVersPoint(self.destination)


class Defenseur(SoccerStrategy):
    def __init__(self):
        self.name="Defenseur"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0,0)
        if (state.ball.position.distance(player.position))>(5*(PLAYER_RADIUS+BALL_RADIUS)):
            if (teamAdverse(teamid)==2):
                pos = Vector2D((1.5/5)*GAME_WIDTH,state.ball.position.y)-player.position
            else:
                pos = Vector2D((3.5/5)*GAME_WIDTH,state.ball.position.y)-player.position
        else:
            pos= state.ball.position-player.position
            
        
        
        if (PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position)):
            shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
            
        return SoccerAction(pos,shoot)
        
    def copy(self):
        return Defenseur()
    def create_strategy(self):
        return Defenseur()
        

class ComposeStrategy(SoccerStrategy):
    def __init__(self, vitesse, tir):
        self.vitesse = vitesse
        self.tir = tir
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        return SoccerAction(self.vitesse.compute_strategy(state, player, teamid).acceleration,self.tir.compute_strategy(state, player, teamid).shoot) 
    def copy(self):
        return ComposeStrategy(self.vitesse.copy(), self.tir.copy())
    def create_strategy(self):
        return ComposeStrategy(self.vitesse, self.tir)