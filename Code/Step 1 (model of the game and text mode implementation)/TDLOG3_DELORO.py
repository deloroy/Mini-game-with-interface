# -*- coding: utf-8 -*-

print("DELORO Yonatan - TDLOG3")

import random

print("Implémentation du modèle et implémentation du jeu en mode texte")
print("----------------------------------------------------------------------")

#dictionnaire associant à une touche "directionnelle" le vecteur déplacement du
#personnage sur le plateau
#variable globale (utilisé par 2 méthodes de Game : MoveAuthorized et EndGame)
directions={"8":(-1,0),"9":(-1,1),"6":(0,1),"3":(1,1),"2":(1,0),"1":(1,-1),
            "4":(0,-1),"7":(-1,-1)}


#1. Grille

class Grid:
    
    def __init__(self,T): 
        assert(T%2!=0) 
        self._taille=T 
        self._grille=[[None for i in range(T)] for j in range(T)] 

    @property   #taille accessible en lecture seulement
    def taille(self):    
        return self._taille

    def __contains__(self,x_y):   #surcharge de "in" 
        (x,y)=x_y
        if (x>=0 and x<self._taille):
            if (y>=0 and y<self._taille):
                return True
        return False

    def __getitem__(self,x_y):    #lecture dans une cellule de la grille  
        assert(x_y in self) 
        (x,y)=x_y
        return self._grille[x][y]
    
    def __setitem__(self,x_y,valeur): #écriture dans une cellule de la grille
        assert(x_y in self) 
        (x,y)=x_y
        self._grille[x][y]=valeur

    def show_grid(self):     
        for i in range(self._taille):
            ligne=[]
            for j in range(self._taille):
                gain=self._grille[i][j]
                ligne.append(str(gain)+(3-len(str(gain)))*" ")
            print(" ".join(ligne))

            
#2. Joueurs
        
class Player:
    def __init__(self,n):
        self._nom=n 
        self._score=0

    @property      #nom accessible en lecture seulement
    def nom(self):   
        return self._nom

    @property      #score accessible en lecture seulement
    def score(self):  
        return self._score
    
    def add_gain(self,gain):  
        self._score+=gain

    def show_score(self):     
        print(self.nom + " : " + str(self.score))

#3. Etats de la partie

class Game():  

    def __init__(self, size, joueur1, joueur2):
        self._Joueurs=[Player(joueur1),Player(joueur2)]  
        self._indice_courant=0
        #égal à 0 ou 1 : self._Joueurs[indice_courant] est le Joueur courant   
        
        self._Plateau=Grid(size)
        self._Personnage=(size//2,size//2)        
        
    def InitRandom(self):
    #Initialise aléatoirement la grille à valeurs dans {5,10,20,50,100,200}
    #On met InitRandom en méthode de Game et non de Grid, car on ne doit pas
    #mettre de gain dans la case initiale du Personnage, au centre de la grille
    #dans l'énoncé du TP mais qu'on pourrait vouloir aussi changer facilement
        
        valeurs_pieces=[5,10,20,50,100,200]
        for x in range(self._Plateau.taille):
            for y in range(self._Plateau.taille):
                if (x,y)==self._Personnage:
                    self._Plateau[x,y]="###"   
                else:
                    self._Plateau[x,y]=random.choice(valeurs_pieces)        

    def MoveAuthorized(self,direction):
    #Renvoit False si la direction choisie par le joueur n'est pas autorisée
    #Sinon, renvoit la nouvelle position du personnage qui a suivi la direction
        
        global directions
        if not direction in directions.keys():
            #la touche ne correspond à aucune direction
            return False
        else:             
            deplacement=directions[direction]
            position_new=(self._Personnage[0]+deplacement[0],
                          self._Personnage[1]+deplacement[1])
            if not position_new in self._Plateau:
                #le personnage sort du format de la grille 
                return False
            else :
                if self._Plateau[position_new]=="X":
                    #le personnage atteint une case déjà visitée (sans gain)
                    return False
            return position_new  #si on arrive là, le mouvement est autorisé                       

    def AskPlayer(self):
    #Demande au joueur de choisir une direction autorisée et la retourne
        
        print("Joueur " + self._Joueurs[self._indice_courant].nom
              + ", veuillez entrer une direction et appuyer sur entrée")
        print("7    8    9")
        print("  \  |  /  ")
        print("4 - ### - 6")
        print("  /  |  \ ")
        print("1    2    3") 
        print("")

        print("Direction choisie : ")
        direction=input()    
        while (self.MoveAuthorized(direction)==False):     
            print("Direction erronée. Veuillez en choisir une autre ")
            direction=input()
        return direction
        
    def PlayStroke(self):
    #Gère le coup d'un joueur (intéraction et actualisation grille/scores)
        
        self._Plateau[self._Personnage]="X"
        #on marque l'absence de gain sur la case de départ du personnage
        
        direction=self.AskPlayer()                        #direction autorisée
        self._Personnage=self.MoveAuthorized(direction)   #mouvement personnage  
        
        self._Joueurs[self._indice_courant].add_gain(self._Plateau[self._Personnage])  
        self._indice_courant=(self._indice_courant+1)%2   #changement du joueur                             

        self._Plateau[self._Personnage]="###"
        #on marque la nouvelle position du personnage dans la grille

    def EndGame(self): 
        global directions
        for deplacement in directions.values():       
            position_new=(self._Personnage[0]+deplacement[0], 
                          self._Personnage[1]+deplacement[1])
            if position_new in self._Plateau:
                if self._Plateau[position_new]!="X":
                    return False
        return True
        
    def Result(self):   
        for i in range(0,2):
            print("Resultat de " + self._Joueurs[i].nom + " : "
                  + str(self._Joueurs[i].score))
        if (self._Joueurs[0].score>self._Joueurs[1].score):
            print("Vainqueur : " + self._Joueurs[0].nom)
        elif (self._Joueurs[0].score<self._Joueurs[1].score):
            print("Vainqueur : " + self._Joueurs[1].nom)
        else:
            print("Match nul")
        print("--------------------------------------------------------------")


    def Show(self):
        print("")
        print("La grille : ")
        self._Plateau.show_grid()
        print("")
        for i in range(0,2):
            self._Joueurs[i].show_score()
        print("")
        print("--------------------------------------------------------------")


#4. Déroulement du jeu

G=Game(7,"N1","N2")
G.InitRandom()
G.Show()
while (not G.EndGame()):
     G.PlayStroke()
     G.Show()
G.Result()
    
    
    


            

    

    
        


                 
