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
            teamAdverse(teamid)  
            shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
        
            
        return SoccerAction(pos,shoot)
    def copy(self):
        return JoueurFonceur()
    def create_strategy(self):
        return JoueurFonceur()
        
        
class AllerVersPoint(SoccerStrategy):
    def __init__(self, destination=Vector2D()):
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
      
class DefenseurContreAttaque(SoccerStrategy):
    def __init__(self):
        self.name="DefenseurContreAttaque"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0,0)
        d = state.ball.position - player.position
        if d.norm > 25 :
            if (teamAdverse(teamid)==2):
                pos = Vector2D((1.2/5)*GAME_WIDTH,state.ball.position.y)-player.position
            else:
                pos = Vector2D((3.7/5)*GAME_WIDTH,state.ball.position.y)-player.position
        else:
            pos= state.ball.position-player.position
            shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
            
        
        
        if (PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position)):
            shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
           
            
        return SoccerAction(pos,shoot)
        
    def copy(self):
        return DefenseurContreAttaque()
    def create_strategy(self):
        return DefenseurContreAttaque()
        
             
        
class GoalContreAttaque(SoccerStrategy):
    def __init__(self):
        self.name="GoalContreAttaque"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0,0)
        d = state.ball.position - player.position
        if d.norm > 30 :
            if (teamAdverse(teamid)==2):
                pos = Vector2D((0.2/5)*GAME_WIDTH,state.ball.position.y)-player.position
            else:
                pos = Vector2D((4.8/5)*GAME_WIDTH,state.ball.position.y)-player.position
        else:
            pos= state.ball.position-player.position
            shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
            
        
        
        if (PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position)):
            shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
           
            
        return SoccerAction(pos,shoot)
        
    def copy(self):
        return GoalContreAttaque()
    def create_strategy(self):
        return GoalContreAttaque()
        
        
class Goal(SoccerStrategy):
    def __init__(self):
        self.name="Defenseur"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0,0)
        d = state.get_goal_center(teamid) - state.ball.position
      
        if d.norm > (0.3)*GAME_WIDTH or player.position.y > (GAME_HEIGHT)*4.0/5 or player.position.y < (GAME_HEIGHT)*1.0/5 and state.ball.position.x<(0.5)*GAME_WIDTH :
        
            acceleration = state.get_goal_center(teamid) - player.position
        else:
            acceleration = state.ball.position-player.position
           
            
        
        
        if (PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position)):
            p = state.get_goal_center(teamAdverse(teamid)) - state.ball.position            
        else:
            acceleration = state.ball.position-player.position
            shoot = Vector2D.create_polar((p.angle)+3.14/8, p.norm)
            acceleration = Vector2D(0,0)
           
            
        return SoccerAction(acceleration,shoot)
        
    def copy(self):
        return Goal()
    def create_strategy(self):
        return Goal()
        
        
class Defenseur(SoccerStrategy):
    def __init__(self):
        self.name="Defenseur"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0,0)
        d = state.get_goal_center(teamid) - state.ball.position
      
        if d.norm > (0.3)*GAME_WIDTH or player.position.y > (GAME_HEIGHT)*4.0/5 or player.position.y < (GAME_HEIGHT)*1.0/5 and state.ball.position.x<(0.5)*GAME_WIDTH :
            if (teamAdverse(teamid)==2):
                pos = Vector2D((1.2/5)*GAME_WIDTH,state.ball.position.y)-player.position
            else:
                pos = Vector2D((3.7/5)*GAME_WIDTH,state.ball.position.y)-player.position
                
        else:
            acceleration = state.ball.position-player.position
            shoot = Vector2D.create_polar((p.angle)+3.14/8, p.norm)
            acceleration = Vector2D(0,0)
           
            
        return SoccerAction(acceleration,shoot)
        
    def copy(self):
        return Defenseur()
    def create_strategy(self):
        return Defenseur()
        
        
class EviteBall(SoccerStrategy):
    def __init__(self):
        self.name="Evite"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0,0)
        d = state.ball.position - player.position
        goalAdverse = state.get_goal_center(teamAdverse(teamid))
        
        
        if (d.norm<=GAME_WIDTH*0.2):
             acceleration = state.ball.speed
        else:
             acceleration = Vector2D (0, d.y)
             
        
        return SoccerAction(acceleration,shoot)
        
    def copy(self):
        return EviteBall()
    def create_strategy(self):
        return EviteBall()
        
            
            
        
        
        
        
'''
       
class Defenseur(SoccerStrategy):
    def __init__(self):
        self.name="Defenseur"
        self.list=[Goal(),AllerVersPoint(),]
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def selector(self,state,player,teamid):
        if (condition pour goal : ball proche des butsd):
            return 0
        if (condition ...) :
            self.list[1].direction = ....
            return 1
        return -1
    
    def compute_strategy(self,state,player,teamid):
        
        idx = self.selector(state,player,teamid)
        return self.list[idx].compute_strategy(state,player,teamid)
     
         shoot = Vector2D(0,0)
        d = state.ball.position - player.position
        goalAdverse = state.get_goal_center(teamAdverse(teamid))
        acceleration = Vector2D (0, d.y)
        if (d.norm>GAME_WIDTH*0.2):
            if (PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position)):
          
                shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
            

        else: 
            acceleration = state.ball.speed
            
                
                 if (state.get_goal_center(teamid) - player.position >(0.1*(GAME_WIDTH))):
                 acceleration = Vector2D(0, state.ball.speed.y)
            
   
                
            
           
            
        return SoccerAction(acceleration,shoot)
        
    def copy(self):
        return Defenseur()
    def create_strategy(self):
        return Defenseur()
        
        
        
class Dribbleur(SoccerStrategy):
    def __init__(self):
        self.name="Dribbleur"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        pos = state.ball.position-player.position
        shoot = Vector2D(0,0)
        if (PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position)):
            teamAdverse(teamid)  
            shoot= Vector2D(0.5,0.5)
        
            
        return SoccerAction(pos,shoot)
    def copy(self):
        return Dribbleur()
    def create_strategy(self):
        return Dribbleur()
        '''
        
        
        
        

        

        
        
