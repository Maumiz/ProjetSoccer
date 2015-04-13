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

#retourne la distance entre le ballon et le joueur adverse
def distAdvBall(state, teamid, player):
    balle = state.ball.position
    adv = joueurAdverseProche(state, teamid, player)
    if (adv!=None):
        return balle.distance(adv)
    else:
        return None

#retourne ma distance au ballon
def distballon(state, player):
    return state.ball.position.distance(player.position)

#retourne les coordonnées de la defense
def defense(teamid):
    if (teamid==1):
        return Vector2D(GAME_WIDTH*0.2, GAME_HEIGHT*0.5)
    else:
        return Vector2D(GAME_WIDTH*0.8, GAME_HEIGHT*0.5)
        
# retourne les coordonnées de mon goal    
def goal(teamid):
    if (teamid==1):
        return Vector2D(GAME_WIDTH*0, GAME_HEIGHT*0.5)
    else:
        return Vector2D(GAME_WIDTH, GAME_HEIGHT*0.5)

#retourne true si mon adversaire est dans ses cages
def estDansCages(state, teamid, player):
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
    if (PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position)):
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
        coord = Vector2D(-1, -1)
        moi = player.position
        if (teamadv==1):
            list_joueurs = state.team1.players
        else:
            list_joueurs = state.team2.players
        for p in list_joueurs:
                if (p.position.distance(moi) < (GAME_WIDTH*0.15) and (abs(moi.y-p.position.y)<GAME_HEIGHT*(0.9))) :
                    coord = p.position
        return coord
        
        
#indique si on a dépasse le joueur adverse proche        
def joueurAdverseDerriere(state, teamid, player, adv):
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
        return Vector2D(GAME_WIDTH*(1.0/5),GAME_HEIGHT*0.5)
    else:
        return Vector2D(GAME_WIDTH*(4.0/5),GAME_HEIGHT*(0.5))


# Retourne True si la balle se trouve dans la surface de rep        
def dansSurface(state, teamid):
    a = Vector2D((GAME_WIDTH*(1.5/5)), (GAME_HEIGHT*(1.5/5)))
    b = Vector2D((GAME_WIDTH*(1.5/5)), (GAME_HEIGHT*(3.5/5)))
    c = Vector2D((GAME_WIDTH*(3.5/5)), (GAME_HEIGHT*(1.5/5)))
    d = Vector2D((GAME_WIDTH*(3.5/5)), (GAME_HEIGHT*(3.5/5)))
    
    if (teamid==1):
        if(state.ball.position.x<(GAME_WIDTH*(1.5/5)) and state.ball.position.y>a.y and state.ball.position.y<b.y) :
            return True
        else:
            return False
    else:
        if(state.ball.position.x>(GAME_WIDTH*(3.5/5)) and state.ball.position.y>c.y and state.ball.position.y<d.y) :
            return True
        else:
            return False

# retourne true si la balle est dans ma moitié de térrain           
def dansTerrain(state, teamid):  
    if (teamid==1):
        if(state.ball.position.x<GAME_WIDTH*0.5):
            return True
        else:
            return False
    else:
        if(state.ball.position.x>GAME_WIDTH*0.5):
            return True
        else:
            return False

#retourne la distance entre le joueur adverse proche et moi        
def distAdv(state, teamid, player):
    moi = player.position
    adv = joueurAdverseProche(state, teamid, player)
    if (adv!=None):
        return (adv - moi).norm
    else:
        return -1
        

       

# Retourne True si mon equipe a la balle        
def quiBalle(state, teamid, player):
    def distABalle(p):
        return state.ball.position.distance(p.position)
    p1= min(state.team1.players, key=distABalle)
    p2= min(state.team2.players, key=distABalle)    
    if distABalle(p1)<distABalle(p2):
        return teamid==1
    else:
        return teamid==2
        
# Indique la distance de mon joueur par rapport à ma surface
def distSurface(state, teamid, player):
    centre = centreSurface(state, teamid, player)
    moi = player.position
    return (centre - moi).norm
    
        
        
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
        self.name = "immobile"
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
        self.name = "haut"
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
        self.name = "bas"
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
        self.name = "gauche"
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
        self.name = "droit"
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
        self.name = "hg"
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
        self.name = "hd"
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
        self.name = "bg"
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
        self.name = "bd"
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
        self.name = "allerverscages"
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