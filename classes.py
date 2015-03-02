# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:58:42 2015

@author: 3301031
"""

from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH 
from soccersimulator import PygletObserver,ConsoleListener,LogListener

#############################################
###################           ###############
##############  FONCTIONS UTILES  ###########
###################           ###############
#############################################

#Donne l'équipe Adverse
def teamAdverse(teamid):
    adv=2
    if (teamid==2):
        adv=1
    return adv
    

#donne les coordonnes du joueur adverse si il est assez proche
def joueurAdverseProche(state, teamid, player):
        teamadv = teamAdverse(teamid)
        coord = None
        if (teamadv==1):
            list_joueurs = state.team1.players
        else:
            list_joueurs = state.team2.players
        for p in list_joueurs:
            if (p.position.distance(player.position) < (GAME_WIDTH*0.2) ) :
                coord = p.position
        return coord
        
        
#indique si on a dépasse le joueur adverse proche        
def joueurAdversaireDerriere(state, teamid, player, adv):
    teamadv = teamAdverse(teamid)
    moi = player.position
    a = False
    if (adv!=None):
        if (teamadv==1):
            if(adv.x > moi.x):
                a = True
            else:
                a = False
        else:
            if(adv.x<moi.x):
                a = True
            else:
                a = False
                    
    return a
    


#renvoie le centre de la droite qui delimite surface de rep
def centreSurface(state, teamid, player):
    if (teamid==1):
        return Vector2D(GAME_WIDTH*(1.0/5),state.get_goal_center(teamid).y)
    else:
        return Vector2D(GAME_WIDTH*(4.0/5),state.get_goal_center(teamid).y)


# indique si mon joueur se trouve dans la surface de rep        
def DansSurface(state, teamid, player):
    a = Vector2D((GAME_WIDTH*(1.0/5)), (GAME_HEIGHT*(1.5/5)))
    b = Vector2D((GAME_WIDTH*(1.0/5)), (GAME_HEIGHT*(3.5/5)))
    c = Vector2D((GAME_WIDTH*(4.0/5)), (GAME_HEIGHT*(1.5/5)))
    d = Vector2D((GAME_WIDTH*(4.0/5)), (GAME_HEIGHT*(3.5/5)))
    
    if (teamid==1):
        if(player.position.x<(GAME_WIDTH*(1.0/5)) and player.position.y>a.y and player.position.y<b.y) :
            return True
        else:
            return False
    else:
        if(player.position.x>(GAME_WIDTH*(4.0/5)) and player.position.y>c.y and player.position.y<d.y) :
            return True
        else:
            return False
            
def distAdv(state, teamid, player):
    acceleration = Vector2D(0,0)
    moi = player.position
    adv = joueurAdverseProche(state, teamid, player)
    if (adv!=None):
        return adv - moi
    else:
        return None
        
    
       
'''  
# Retourne True si mon equipe a la balle        
def quiABalle(state, teamid, player, adv):
    teamadv = teamAdverse(teamid)
    if (teamadv==1):
        for p in state.team1.players:
            a = min(state.ball.position.distance(p.position))
        for p in state.team2.players:
            b = min(state.ball.position.distance(p.position))
        if (a<b):
            return False
        else:
            return True
    else: 
        for p in state.team1.players:
            a = min(state.ball.position.distance(p.position))
        for p in state.team2.players:
            b = min(state.ball.position.distance(p.position))
        if (a<b):
            return True
        else:
            return False
'''
    

    
    
            
            
###################################
######### CLASSES #################
###################################


#Le joueur se déplace aléatoirement et ne tire pas
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
        

#Joueur qui fonce vers cages adverses avec la balle
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
            shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
        
            
        return SoccerAction(pos,shoot)
    def copy(self):
        return JoueurFonceur()
    def create_strategy(self):
        return JoueurFonceur()
        
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
    def copy(self):
        return AllerVersPoint(self.destination)
    def create_strategy(self):
        return AllerVersPoint(self.destination)
        

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
        if (PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position)): 
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
            
    def create_strategy(self):
        return Degagement()
        
class Defenseur(SoccerStrategy):
    def __init__(self, dest=Vector2D()):
        self.dest = AllerVersPoint(Vector2D()) 
        self.degage = Degagement()
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        self.dest.destination = state.ball.position
        if (PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position)):
            return self.degage.compute_strategy(state, player, teamid)
        else:
            return self.dest.compute_strategy(state, player, teamid)
    def create_strategy(self):
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
        

class Intercepteur(SoccerStrategy):
    def __init__(self):
        self.suivre = Suiveur()
        self.defendre = Defenseur()
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        if teamid == 1:
            if state.ball.position.x> centreSurface(state, teamid, player).x:
                return self.suivre.compute_strategy(state,player,teamid)
            else:
                return self.defendre.compute_strategy(state,player,teamid)
        else:
            if state.ball.position.x< centreSurface(state, teamid, player).x:
                return self.suivre.compute_strategy(state,player,teamid)
            else:
                return self.defendre.compute_strategy(state,player,teamid)
    def create_strategy(self):
        return Intercepteur()

    
# permet de composer une strategie qui prend le deplacement de l'une et le tir de l'autre
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
  
# Un defenseur qui vole la balle et fonce vers les cages    
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
        
            
            
#Un goal qui vole la balle et fonce vers cages
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
        
 
# Un goal qui degage la balle puis revient aux cages       
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
        
        if (DansSurface(state, teamid, player)==False):
        
            acceleration = state.get_goal_center(teamid) - player.position
            
            if (d.norm)<(GAME_WIDTH*0.3):
                 acceleration = state.ball.position-player.position
                 
        else:
            acceleration = state.get_goal_center(teamid) - player.position
            
            if (d.norm)<(GAME_WIDTH*0.3):
                 acceleration = state.ball.position-player.position
                 
                       
        if (PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position)):
            p = state.get_goal_center(teamAdverse(teamid)) - state.ball.position            
            shoot = Vector2D.create_polar((p.angle)+3.14/8, p.norm)
            acceleration = Vector2D(0,0)
           
        return SoccerAction(acceleration,shoot)
        
    def copy(self):
        return Goal()
    def create_strategy(self):
        return Goal()
        
'''  
# Un defenseur qui dégage la balle   
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
'''        
      
# Un dribbleur qui contourne l'adversaire et qui pousse la balle par des petits coups. Une fois qu'il a contourné l'adversaire, il fonce vers les buts opposés.
# Probleme parfois lors de croisement de certains adversaires, il les contourne alors qu'il ne devrait pas car ils sont loins, peut etre probleme avec les 
# coordonnes y?
class Dribbleur(SoccerStrategy):
    def __init__(self):
        self.name="Dribbleur"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        moi = player.position
        adv = joueurAdverseProche(state, teamid, player)
        shoot = Vector2D(0,0)
  
        if (adv!=None):
            tir= adv - moi
            a = state.get_goal_center(teamAdverse(teamid))-player.position
            if (adv.y<moi.y):
                shoot = Vector2D.create_polar((tir.angle)+0.75, 1)
                acceleration = state.ball.position - player.position
                if (joueurAdversaireDerriere(state, teamid, player, adv)==True):
                    shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
                else:
                    shoot = Vector2D.create_polar((tir.angle)+0.75, 1)
                    
            else:
                shoot = Vector2D.create_polar((tir.angle)-0.75, 1)
                acceleration = state.ball.position - player.position
                if (joueurAdversaireDerriere(state, teamid, player, adv)==True):
                    shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
                else:
                    shoot = Vector2D.create_polar((tir.angle)+0.75, 1)
        else :
            shoot = Vector2D.create_polar((state.get_goal_center(teamAdverse(teamid))-player.position).angle, 1)
            acceleration = state.ball.position - player.position
            
        return SoccerAction(acceleration,shoot)
    def copy(self):
        return Dribbleur()
    def create_strategy(self):
        return Dribbleur()
        
'''   
class DefAtt(SoccerStrategy):
    def __init__(self):
        self.attaque=Dribbleur()
        self.defense=
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
'''        
        
        


'''
class DefenseurProf(SoccerStrategy):
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
     
'''
