# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:58:42 2015

@author: 3301031
"""

from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH, GAME_GOAL_HEIGHT
from soccersimulator import PygletObserver,ConsoleListener,LogListener

#############################################
###################           ###############
##############  FONCTIONS UTILES  ###########
###################           ###############
#############################################

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
        return adv - moi
    else:
        return None
        

       

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
        if (balleProche):    
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

# Le joueur retourne en défense        
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

# Degagement utilisé par la classe intercepteur        
class Degagement1(SoccerStrategy):
    def __init__(self):
        self.action=ComposeStrategy(AllerVersBalle(), Degagement())
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        return self.action.compute_strategy(state,player,teamid)

        
#Lle joueur s'aligne par apport au ballon        
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

# un goal qui s'aligne par apport à la balle        
class golAligne(SoccerStrategy):
    def __init__(self):
        pass
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        if estDansCages(state, teamid, player):
            acceleration = Vector2D(state.get_goal_center(teamid).x, state.ball.position.y)
            shoot = Vector2D(0,0)
        return SoccerAction(acceleration,shoot)
        
#defenseur qui degage la balle si le joueur adverse est dans ma moitié de terrain     
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
   
'''class Defenseur1(SoccerStrategy):
    def __init__(self, dest=Vector2D()):
        self.dest = AllerVersPoint(Vector2D())
        self.degage = Degagement1()
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        if(dansTerrain(state, teamid) and quiABalle(state, teamid)==False):
            return self.degage.compute_strategy(state,player,teamid)
            print degage
        else:
            self.dest.destination = defense(teamid)
            return self.dest.compute_strategy(state,player,teamid)'''
            
#Suit le joueur qui à la balle en se placant entre les cages et le joueur adverse
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
        
#Suit le joueur adverse grace à strategie suiveur puis lorsque le joueur rentre dans la surface de rep, il degage la balle
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
        if (balleProche):
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
            
        
        
        if (balleProche):
            shoot= (state.get_goal_center(teamAdverse(teamid))-player.position)
           
            
        return SoccerAction(pos,shoot)
        
    def copy(self):
        return GoalContreAttaque()
    def create_strategy(self):
        return GoalContreAttaque()

# Un goal qui dégage la balle et s'aligne par rapport au ballon      
class Goal1(SoccerStrategy):
    def __init__(self, dest = Vector2D()):
        self.dest = AllerVersPoint(Vector2D())
        self.degage = Degagement()
        self.aligne = aligne()
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        bds = dansSurface(state, teamid) # bds = balledanssurface #
        if bds:
            if player.position.y > (1.3)*GAME_WIDTH :
                self.dest.destination = Vector2D (state.get_goal_center(teamid).x, state.ball.position.y) 
            else:
                self.dest.destination = state.ball.position
                if((PLAYER_RADIUS+BALL_RADIUS)>=(state.ball.position.distance(player.position))):
                    return self.degage.compute_strategy(state, player, teamid)
                else:
                   return self.dest.compute_strategy(state, player, teamid)
        else:
            self.dest.destination = Vector2D (state.get_goal_center(teamid).x, state.ball.position.y)
            return self.dest.compute_strategy(state, player, teamid)
    def create_strategy(self):
        return Goal1()

# Un goal qui degage la balle puis revient aux cages       
class Goal2(SoccerStrategy):
    def __init__(self):
        pass
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0,0)
        d = state.get_goal_center(teamid) - state.ball.position
        
        if (dansSurface(state, teamid)==False):
        
            acceleration = state.get_goal_center(teamid) - player.position
            
            if (d.norm)<(GAME_WIDTH*0.3):
                 acceleration = state.ball.position-player.position
                 
        else:
            acceleration = state.get_goal_center(teamid) - player.position
            
            if (d.norm)<(GAME_WIDTH*0.3):
                 acceleration = state.ball.position-player.position
                 
                       
        if balleProche(state, player):
            p = state.get_goal_center(teamAdverse(teamid)) - state.ball.position            
            shoot = Vector2D.create_polar((p.angle)+3.14/8, p.norm)
            acceleration = Vector2D(0,0)
           
        return SoccerAction(acceleration,shoot)

        
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
        acceleration = state.ball.position - player.position
        a = state.get_goal_center(teamAdverse(teamid))-player.position
        
        if (adv!=None):
            tir= adv - moi

            if (adv.y<moi.y) and balleProche(state, player):
                shoot = Vector2D.create_polar((tir.angle)+0.75, 1.75)
                acceleration = state.ball.position - player.position
                if (joueurAdverseDerriere(state, teamid, player, adv)==True) and balleProche(state, player):
                    shoot= a
                elif(balleProche(state,player)):
                    shoot = Vector2D.create_polar((tir.angle)+0.75, 1.75)
                    
            elif (balleProche(state,player)):
                shoot = Vector2D.create_polar((tir.angle)-0.75, 1.75)
                acceleration = state.ball.position - player.position
                if (joueurAdverseDerriere(state, teamid, player, adv)==True) and balleProche(state,player):
                    shoot= a
                elif(balleProche(state,player)):
                    shoot = Vector2D.create_polar((tir.angle)+0.75, 1.75)
        elif(balleProche(state,player)):
            shoot = Vector2D.create_polar(a.angle, 1.75)
            acceleration = state.ball.position - player.position
            
        return SoccerAction(acceleration,shoot)
    def copy(self):
        return Dribbleur()
    def create_strategy(self):
        return Dribbleur()
        
#Tire dans la direction opposé au gol adverse en utilisant estdanscages
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
        
# Attaquant qui combine mon dribbleur et mon tireur --> très efficace
class Attaquant(SoccerStrategy):
    def __init__(self):
        self.dribble=Dribbleur()
        self.tir=ComposeStrategy(AllerVersBalle(), Tireur())
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        moi = player.position
        if (teamid == 1):
            if (moi.x>GAME_WIDTH*0.95):
                return self.tir.compute_strategy(state, player, teamid)
            else:
                return self.dribble.compute_strategy(state,player,teamid)
        else:
            if(moi.x<GAME_WIDTH*0.05):
                return self.tir.compute_strategy(state, player, teamid)
            else:
                return self.dribble.compute_strategy(state,player,teamid)
