# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 19:11:22 2015

@author: 3301031
"""

""" Stratégies simples dérivées de mes stratégies du fichier classes.py, afin de pouvoir faire le joueur intelligent sans des strats compliquées"""

from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH, GAME_GOAL_HEIGHT
from soccersimulator import PygletObserver,ConsoleListener,LogListener
import math


##################################
####### FONCTIONS UTILES##########
##################################


#retourne les coordonnées de la defense
def defense(teamid):
    if (teamid==1):
        return Vector2D(GAME_WIDTH*0.2, GAME_HEIGHT*0.5)
    else:
        return Vector2D(GAME_WIDTH*0.8, GAME_HEIGHT*0.5)

#retourne les coordonnées de meon goal    
def goal(teamid):
    if (teamid==1):
        return Vector2D(GAME_WIDTH*0, GAME_HEIGHT*0.5)
    else:
        return Vector2D(GAME_WIDTH, GAME_HEIGHT*0.5)

#retourne true si mon adversaire est dans ses cages
def estDansCages(state, player, teamid):
    adv = joueurAdverseProche(state, teamid, player)
    teamadv = teamAdverse(teamid)
    if(adv!= None):
        if(teamadv==1):
            return ((adv.x<GAME_WIDTH*1.0/10) and (adv.y<state.get_goal_center(teamadv).y+(((GAME_GOAL_HEIGHT/2)*(4.0/5))))\
                        and (adv.y>state.get_goal_center(teamadv).y-((GAME_GOAL_HEIGHT/2)*(4.0/5))))
        else:
            return ((adv.x>GAME_WIDTH*9.0/10) and (adv.y<state.get_goal_center(teamadv).y+((GAME_GOAL_HEIGHT/2)*(4.0/5))) \
                        and (adv.y>state.get_goal_center(teamadv).y-((GAME_GOAL_HEIGHT/2)*(4.0/5))))
    else:
        return False
                
                
                
#Retourne True si la balle est proche
def balleProche(state, player):
    if ((PLAYER_RADIUS+BALL_RADIUS))>=(state.ball.position.distance(player.position)):
        return True
    else:
        return False

#Donne l'équipe Adverse
def teamAdverse(teamid):
    adv=2
    if (teamid==2):
        adv=1
    return adv
    
#Donne le centre des cages adverses
def cagesAdverse(teamid):
    return state.get_goal_center(teamAdverse(teamid))

#donne les coordonnes du joueur adverse si il est assez proche
def joueurAdverseProche(state, teamid, player):
        teamadv = teamAdverse(teamid)
        coord = None
        moi = player.position
        if (teamadv==1):
            list_joueurs = state.team1.players
        else:
            list_joueurs = state.team2.players
        for p in list_joueurs:
                if (p.position.distance(moi) < (GAME_WIDTH*0.15) and (abs(moi.y-p.position.y)<GAME_HEIGHT*(0.9))) :
                    coord = p.position
        return coord
        
                                ###########################################      
                                ###############STRATEGIES############
                                ###########################################

##################
###DEPLACEMENTS###
##################

# Joueur Random qui se déplace et shoote aléatoirement
class RandomStrategy(SoccerStrategy):
    def __init__(self):
        self.name="random"
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

# Le joueur arrete de bouger et de tirer
class Immobile(SoccerStrategy):
    def __init__(self):
        self.name = "Immobile"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0, 0)
        acceleration = Vector2D(0, 0)
        return SoccerAction(acceleration, shoot)

#Le Joueur se déplace en haut
class Haut(SoccerStrategy):
    def __init__(self):
        self.name = "Haut"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0, 0)
        acceleration = Vector2D(player.position.x, player.position.y+0.5) - player.position
        return SoccerAction(acceleration, shoot)
   
#Le joueur se déplace en bas     
class Bas(SoccerStrategy):
    def __init__(self):
        self.name = "Bas"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0, 0)
        acceleration = Vector2D(player.position.x, player.position.y-0.5) - player.position
        return SoccerAction(acceleration, shoot)

#Le joueur se déplace à gauche       
class Gauche(SoccerStrategy):
    def __init__(self):
        self.name = "Gauche"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0, 0)
        acceleration = Vector2D(player.position.x-0.5, player.position.y) - player.position
        return SoccerAction(acceleration, shoot)

#Le joueur se déplace à droite       
class Droit(SoccerStrategy):
    def __init__(self):
        self.name = "Droit"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0, 0)
        acceleration = Vector2D(player.position.x+0.5, player.position.y) - player.position
        return SoccerAction(acceleration, shoot)

#Le joueur se déplace en haut à gauche        
class HG(SoccerStrategy):
    def __init__(self):
        self.name = "HG"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0, 0)
        acceleration = Vector2D(player.position.x-0.5, player.position.y+0.5) - player.position
        return SoccerAction(acceleration, shoot)

#Le joueur se déplace en haut à droite        
class HD(SoccerStrategy):
    def __init__(self):
        self.name = "HD"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0, 0)
        acceleration = Vector2D(player.position.x+0.5, player.position.y+0.5) - player.position
        return SoccerAction(acceleration, shoot)

#Le joueur se déplace en bas à gauche        
class BG(SoccerStrategy):
    def __init__(self):
        self.name = "BG"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0, 0)
        acceleration = Vector2D(player.position.x-0.5, player.position.y-0.5) - player.position
        return SoccerAction(acceleration, shoot)

#Le joueur se déplace en bas à droite    
class BD(SoccerStrategy):
    def __init__(self):
        self.name = "BD"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0, 0)
        acceleration = Vector2D(player.position.x+0.5, player.position.y-0.5) - player.position
        return SoccerAction(acceleration, shoot)
        
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
        self.name = "allerversballe"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        self.dest.destination = state.ball.position
        return self.dest.compute_strategy(state,player,teamid)

# Le joueur retourne aux cages        
class AllerVersCages(SoccerStrategy):
    def __init__(self):
        self.dest = AllerVersPoint(Vector2D())
        self.name = "allerversballe"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        if (teamid == 1):
            self.dest.destination = state.get_goal_center(teamid)+Vector2D(10, 0)
        else:
            self.dest.destination = state.get_goal_center(teamid)-Vector2D(10, 0)
        return self.dest.compute_strategy(state,player,teamid)
        
# Retourne en défense
class AllerDef(SoccerStrategy):
    def __init__(self):
        self.dest = AllerVersPoint(Vector2D())
        self.name = "allerdef"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        self.dest.destination = defense(teamid)
        return self.dest.compute_strategy(state,player,teamid)
        
# Le joueur s'aligne par rapport aux coordonées y du ballon        
class aligne(SoccerStrategy):
    def __init__(self):
        self.aligne = "aligne"
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
        
# Le joueur se place entre la distance de mes buts et de la balle        
class Suiveur(SoccerStrategy):
    def __init__(self, dest=Vector2D()):
        self.dest = AllerVersPoint(Vector2D())
        self.name = "suiveur"
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
        

###################
#######TIRS########
###################
        
        
#degage la balle dans un angle orienté vers le haut
class TirHaut(SoccerStrategy):
    def __init__(self):
        pass
        self.name = "tirhaut"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        acceleration = Vector2D(0,0)
        goaladv = state.get_goal_center(teamAdverse(teamid))
        dist = goaladv - state.ball.position
        if (balleProche(state, player)): 
            shoot= Vector2D.create_polar((dist.angle)-0.25, 2)
        else:
            shoot = Vector2D(0,0)
        return SoccerAction(acceleration, shoot)

# dégage la balle dans un angle orienté vers le bas     
class TirBas(SoccerStrategy):
    def __init__(self):
        pass
        self.name = "tirbas"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        acceleration = Vector2D(0,0)
        goaladv = state.get_goal_center(teamAdverse(teamid))
        dist = goaladv - state.ball.position
        if (balleProche(state, player)): 
            shoot= Vector2D.create_polar((dist.angle)+0.25, 2)
        else:
            shoot = Vector2D(0,0)
        return SoccerAction(acceleration, shoot)

# dégage la balle dans le sens opposé        
class TirOppose(SoccerStrategy):
    def __init__(self):
        pass
        self.name = "tiropose"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        acceleration = Vector2D(0,0)
        goaladv = state.get_goal_center(teamAdverse(teamid))
        dist = goaladv - state.ball.position
        if (balleProche(state, player)): 
            shoot= Vector2D.create_polar((dist.angle)+math.pi, 1)
        else:
            shoot = Vector2D(0,0)
        return SoccerAction(acceleration, shoot)

# Tire vers les cages adverses    
class TirCages(SoccerStrategy):
    def __init__(self):
        pass
        self.name = "tircages"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        acceleration = Vector2D(0,0)
        goaladv = state.get_goal_center(teamAdverse(teamid))
        if (balleProche(state, player)): 
            shoot= goaladv-state.ball.position
        else:
            shoot = Vector2D(0,0)
        return SoccerAction(acceleration, shoot)
        
        
#################################
##### DEPLACEMENTS ET TIRS ######
#################################

# Un joueur qui fonce vers balle et qui tire vers cages adverses
class JoueurFonceur(SoccerStrategy):
    def __init__(self):
        self.name="fonceur"
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
 
# Va vers la balle et tire vers le bas       
class AllerTirerBas(SoccerStrategy):
    def __init__(self):
        self.name="allertirerbas"
        self.bouger = AllerVersBalle()
        self.tir = TirBas()
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        if (balleProche(state, player)):
            return self.tir.compute_strategy(state, player, teamid)
        else:
            return self.bouger.compute_strategy(state, player, teamid)
            
# Va vers la balle et tire vers les cages adverses           
class AllerTirerCages(SoccerStrategy):
    def __init__(self):
        self.name="allertirercages"
        self.bouger = AllerVersBalle()
        self.tir = TirCages()
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        if (balleProche(state, player)):
            return self.tir.compute_strategy(state, player, teamid)
        else:
            return self.bouger.compute_strategy(state, player, teamid)

# Va vers la balle et tire vers le haut            
class AllerTirerHaut(SoccerStrategy):
    def __init__(self):
        self.name="allertirerhaut"
        self.bouger = AllerVersBalle()
        self.tir = TirHaut()
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        if (balleProche(state, player)):
            return self.tir.compute_strategy(state, player, teamid)
        else:
            return self.bouger.compute_strategy(state, player, teamid)

# stratégie de tir pareille que dans celle de classes.py         
class Tireur(SoccerStrategy):
    def __init__(self):
        self.name = "tireur"
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