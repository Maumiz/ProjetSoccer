# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 19:11:22 2015

@author: 3301031
"""
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
        if (balleProche):    
            shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
        return SoccerAction(pos,shoot)
    
        
# Le joueur va vers un point précis du terrain passé en paramètre        
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


# Le joueur va vers la balle        
class AllerVersBalle(SoccerStrategy):
    def __init__(self):
        self.dest = AllerVersPoint(Vector2D())
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        self.dest.destination = state.ball.position
        return self.dest.compute_strategy(state,player,teamid)
        
#degage la balle dans l'angle opposé à l'adversaire
class Degagement(SoccerStrategy):
    def __init__(self):
        pass
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        acceleration = Vector2D(0,0)
        dist = distAdv(state, teamid, player)
        adv = joueurAdverseProche(state, teamid, player)
        moi = player.position
        if (balleProche): 
            if (adv!=None):
                if (adv.y<moi.y):
                    shoot= Vector2D.create_polar((dist.angle)+0.75, state.get_goal_center(teamAdverse(teamid)).norm)
                else:
                    shoot= Vector2D.create_polar((dist.angle)-0.75, state.get_goal_center(teamAdverse(teamid)).norm)
            else:
                shoot = state.get_goal_center(teamAdverse(teamid)) - player.position
        else:
            shoot = Vector2D(0,0)
        return SoccerAction(acceleration, shoot)
        

class AllerDef(SoccerStrategy):
    def __init__(self):
        self.dest = AllerVersPoint(Vector2D())
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        self.dest.destination = defense(teamid)
        return self.dest.compute_strategy(state,player,teamid)
        
        
class aligne(SoccerStrategy):
    def __init__(self):
        pass
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        acceleration = Vector2D(player.position.x, state.ball.position.y)
        shoot = Vector2D(0,0)
        return SoccerAction(acceleration, shoot)
    def aligne(self):
        return Defenseur()
        
        
class Suiveur(SoccerStrategy):
    def __init__(self, dest=Vector2D()):
        self.dest = AllerVersPoint(Vector2D())
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        self.dest.destination = state.ball.position + state.get_goal_center(teamid)
        self.dest.destination.product(0.5)
        return self.dest.compute_strategy(state,player,teamid)
    def create_strategy(self):
        return Suiveur()
        
class AllerDef(SoccerStrategy):
    def __init__(self):
        self.dest = AllerVersPoint(Vector2D())
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        self.dest.destination = goal(teamid)
        return self.dest.compute_strategy(state,player,teamid)
        
class Tireur(SoccerStrategy):
    def __init__(self):
        pass
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        pos = Vector2D(0,0)
        teamadv = teamAdverse(teamid)
        adv = joueurAdverseProche(state, teamid, player)
        print adv
        moi = player.position
        goalhaut= state.get_goal_center(teamAdverse(teamid))+Vector2D(0,((GAME_GOAL_HEIGHT/2)*(3.8/5)))
        goalbas= state.get_goal_center(teamAdverse(teamid))-Vector2D(0, ((GAME_GOAL_HEIGHT/2)*(3.8/5)))
        danscages = estDansCages(state, player, teamid)
        if (balleProche(state, player)):
                if (danscages) and (adv!=None):
                    if (adv.y<=state.get_goal_center(teamadv).y):
                        shoot = goalhaut - moi
                    else:
                        shoot = goalbas - moi
                else :
                    shoot = state.get_goal_center(teamadv)- moi
        else:
            shoot = Vector2D(0,0)
            
        return SoccerAction(pos, shoot)