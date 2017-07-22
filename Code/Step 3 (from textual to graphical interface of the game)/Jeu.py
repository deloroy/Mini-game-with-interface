#Pour moi:
#c:\Users\Martine\Miniconda3\python.exe
#"C:\Users\Martine\Desktop\IMI\TDLOG\DELORO_TDLOG41\DELORO_TDLOG4\Jeu.py"     
# -*- coding: utf-8 -*-                                                                

#DELORO Yonatan 

import random
import math
import copy
import csv

#dictionnaire associant à une touche "directionnelle" le vecteur déplacement du
#personnage sur le plateau
#variable globale (utilisé par 2 méthodes de Game : NewPosition et EndGame)
directions={"8":(-1,0),"9":(-1,1),"6":(0,1),"3":(1,1),"2":(1,0),"1":(1,-1),
            "4":(0,-1),"7":(-1,-1)}

valeurs_pieces=[5,10,20,50,100,200]

#0. Définition des exceptions


class EvenSize(Exception):    #taille de la grille paire 
    pass

class UnauthorizedMove(Exception): #mouvement non autorisé du personnage
    pass

#1. Grille    
    
class Grid:
    
    def __init__(self,T): 
        self._taille=T 
        if (T%2==0):
            raise EvenSize  #levée de l'exception EvenSize
        self._grille=[[None for i in range(T)] for j in range(T)] 
        
    @property   #taille accessible en lecture seulement
    def taille(self):    
        return self._taille

    def __contains__(self,x_y):   #surcharge de "in" 
        (x,y)=x_y
        return x>=0 and x<self._taille and y>=0 and y<self._taille

    def __getitem__(self,x_y):    #lecture dans une cellule de la grille
        assert(x_y in self) 
        (x,y)=x_y
        return self._grille[x][y]
    
    def __setitem__(self,x_y,valeur): #écriture dans une cellule de la grille
        assert(x_y in self) 
        (x,y)=x_y
        self._grille[x][y]=valeur

    def __str__(self): 
        s=""
        for i in range(self._taille):
            for j in range(self._taille):
                gain=self._grille[i][j]
                s+=str(gain)+(3-len(str(gain)))*" " + " " 
            s+="\n"
        return s
        
    def InitRandom(self):
    #Initialise aléatoirement la grille (valeurs choisies dans valeurs_pieces)
        global valeurs_pieces
        for x in range(self._taille):
            for y in range(self._taille):
                self._grille[x][y]=random.choice(valeurs_pieces)        
    
    def LoadFromFile(self, file):       
    #Vérifie que le "tableau" du fichier CSV est carré de taille impaire, puis 
    #initialise la grille aux valeurs de ce "tableau", et réajuste la taille de
    #la grille en conséquence
        with open(file,'r') as fichier:
             c=csv.reader(fichier)
             tab=[]                       
             for ligne in c:
                 l=[]
                 for i in range(len(ligne)):
                     l.append(int(ligne[i]))
                 tab.append(l)
                 
        assert(len(tab[0])==len([l[0] for l in tab]))  #grille carrée
        assert(len(tab[0])%2!=0)                       #grille impaire
        # Si la grille du fichier est de taille paire ici, on s'arrête car on
        #considère l'erreur "irrécupérable" : on ne veut pas travailler sur
        #une autre donnée que celle contenue dans le fichier. 
        #On met donc sciemment un assert et non une exception

        self._grille=copy.deepcopy(tab)      
        self._taille=len(self._grille[0])

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
    
    def __iadd__(self,gain):  #surcharge de +=
        self._score+=gain
        return self

    def __str__(self):      
        return self.nom + " : " + str(self.score)

#3. Etats de la partie

class Game():  

    def __init__(self, size, joueur1, joueur2, joueur1_to_play): 
        #joueur1_to_play est un booléen indiquant si joueur1 est le 1er à jouer
        
        self._Joueurs=[Player(joueur1),Player(joueur2)]  
                
        if joueur1_to_play:
           self.indice_courant=0
        else:
           self.indice_courant=1
        #self._Joueurs[indice_courant] est le Joueur courant           
        
        try:
            self._Plateau=Grid(size) 
            self._Personnage=(size//2,size//2) 
        except EvenSize:
            #si la taille est paire, on prend la décision de l'incrémenter
            #de 1 si la grille ne provient pas d'un fichier. Si elle en provient,
            #on ne change pas sa taille (on ne va pas inventer des données
            #pour compléter le fichier si la taille est paire)
            #Ces choix restent bien sûr arbitraires et discutables.
            print("La taille de la grille doit être impaire. La taille que vous"
            +" avez choisie a été incrémentée automatiquement de 1. Si vous"
            +" avez toutefois choisi d'importer une grille depuis un fichier"
            +" au lieu d'initialiser la grille aléatoirement, la taille sera"
            +" ajustée à celle du fichier et on choisit de ne pas la modifier.")
            self._Plateau=Grid(size+1) 
            self._Personnage=((size+1)//2,(size+1)//2) 
        #on corrige l'exception ici car c'est ici que la question de positionner 
        #le personnage au centre de la grille se pose
            
    def InitRandom(self):
        self._Plateau.InitRandom()
        self._Plateau[self._Personnage]="###"
        
    def LoadFromFile(self, file):
        self._Plateau.LoadFromFile(file)
        self._Personnage=(self._Plateau.taille//2,self._Plateau.taille//2)
        #repositionnement du personnage car la taille de la grille a été
        #réinitialisée à celle du fichier
        self._Plateau[self._Personnage]="###"

    def NewPosition(self,direction):
    #Retourne la nouvelle position du personnage si la direction choisie par le
    #joueur est autorisée. Sinon, ne retourne rien mais lève UnauthorizedMove.
        
        global directions
        if direction in directions.values():
            #la touche correspond à une direction
            (dx,dy)=direction
            position_new=(self._Personnage[0]+dx, self._Personnage[1]+dy)
            if position_new in self._Plateau:
                #le personnage reste dans le format de la grille 
                if (self._Plateau[position_new]!=0 \
                    and self._Plateau[position_new]!="###"):
                    #le personnage atteint une case avec un gain 
                    return position_new   #le mouvement est autorisé
        raise UnauthorizedMove   #levée de l'exception

    def AskPlayer(self):
    #Affiche un message demandant au joueur de choisir une direction
        print("7    8    9")
        print("  \  |  /  ")
        print("4 - ### - 6")
        print("  /  |  \ ")
        print("1    2    3") 
        print("")
        print(self._Joueurs[self.indice_courant].nom
              + ", veuillez entrer une direction et appuyer sur entrée : ")        

        
    def PlayStroke(self, direction):
    #Actualise la grille, les scores et gère le changement de joueur à partir 
    #de la direction choisie par l'utilisateur
        
        self._Plateau[self._Personnage]=0
        #on marque l'absence de gain sur la case de départ du personnage

        self._Personnage=self.NewPosition(direction)   #mouvement personnage  
        
        self._Joueurs[self.indice_courant]+=self._Plateau[self._Personnage] 
        self.indice_courant=(self.indice_courant+1)%2   #changement du joueur                             

        self._Plateau[self._Personnage]="###"
        #on marque la nouvelle position du personnage dans la grille
        
    def EndGame(self): 
        global directions
        for (dx,dy) in directions.values():       
            position_new=(self._Personnage[0]+dx, self._Personnage[1]+dy)
            if position_new in self._Plateau:
                if self._Plateau[position_new]!=0:
                    return False
        return True
            
    def Result(self):         
        if (self._Joueurs[0].score>self._Joueurs[1].score):
            return "Vainqueur : " + self._Joueurs[0].nom
        elif (self._Joueurs[0].score<self._Joueurs[1].score):
            return "Vainqueur : " + self._Joueurs[1].nom
        return "Match nul"        
        
        
    def Show(self):
        print("")
        print("La grille : ")
        print(self._Plateau)
        print("")
        for joueur in self._Joueurs:
            print(joueur)
        print("")
        print("--------------------------------------------------------------")


    def MinMax(self, i, profondeur, is_max):
        #Renvoit le couple (gain,coup) où "coup" est la direction du personnage
        #qui maximise/minimise (selon is_max=True/False) le "gain" donné par 
        #l'évaluation de la configuration pour le joueur d'indice i
        # à une profondeur aussi grande que possible dans la
        #limite de "profondeur" (jusqu'à la fin du jeu si on peut à temps).
        
        #Critères choisis pour l'évaluation d'une configuration :
    #1. L'IA favorise toujours les configurations gagnantes et choisit parmi 
    #les gagnantes celle qui augmente l'écart entre les 2 joueurs. 
    #2. L'IA défavorise toujours les configurations perdantes et choisit, si
    #elles le sont toutes, celle conduisant au plus petit écart
    #3. L'IA choisit, entre deux configurations où le jeu n'est pas fini,
    #celle qui maximise la différence entre son score et celui de l'adversaire
    #4. L'IA est "indifférent" entre une configuration de match nul et 
    #une configuration où le jeu n'est pas fini et où les joueurs 
    #sont à égalité
        #On construit donc une fonction score satisfaisant ces critères
            
        #PS : On passe l'indice du joueur à évaluer en paramètre, i, car 
        #self.indice_courant va être modifié lors des appels récursifs 
        #(lors de la simulation des coups)
        
        global directions
        global valeurs_pieces
        sup_diff = max(valeurs_pieces)*(self._Plateau.taille**2) 
        #une borne supérieure de l'ensemble des différences de scores possibles
            
        if self.EndGame():
            diff=self._Joueurs[i].score-self._Joueurs[(i+1)%2].score
            if diff>0:
                return (sup_diff + diff, (0,0)) 
                #avec le "sup_diff", la stratégie l'emporte sur toutes celles
                #qui ne gagnent pas ; et avec le "diff", elle l'emporte sur 
                #les stratégies gagnantes qui conduisent à un écart moins grand
            elif diff<0:
                return (-sup_diff + diff, (0,0))
            else:
                return (0,(0,0))
        elif profondeur<=0:  
            return (self._Joueurs[i].score-self._Joueurs[(i+1)%2].score, (0,0)) 
        
        else:
            if is_max:
                #le joueur i veut maximiser l'évaluation de sa position
               (gain_max,coup_max)=(-math.inf,(0,0))
               for direction in directions.values(): #coup envisageable 
                   try:
                      Jeu2=copy.deepcopy(self) 
                      Jeu2.PlayStroke(direction)  
                      #simulation du coup sur copie du jeu
                      (gain,coup)=Jeu2.MinMax(i,profondeur-1,False) 
                      #evaluation du coup en scorant la position du joueur i 
                      #après le meilleur coup que pourra jouer son 
                      #adversaire à partir de cette nouvelle configuration
                      if gain>gain_max: #choix du coup qui maximise ce score
                         gain_max=gain   
                         coup_max=direction     
                   except UnauthorizedMove:       
                       pass     #on n'étudie pas cette possibilité de coup
               return (gain_max,coup_max)
            else:
               #l'adversaire du joueur i veut minimiser l'évaluation de 
               #la position du joueur i
               (gain_min,coup_min)=(math.inf,(0,0))
               for direction in directions.values():
                   try:
                      Jeu2=copy.deepcopy(self)  
                      Jeu2.PlayStroke(direction)
                      #simulation du coup sur copie du jeu
                      (gain,coup)=Jeu2.MinMax(i,profondeur-1,True)
                      #evaluation du coup en scorant la position du joueur i 
                      #après le meilleur coup que pourra jouer celui-ci
                      #à partir de cette nouvelle configuration
                      if gain<gain_min:  #choix du coup qui minimise ce score
                         gain_min=gain
                         coup_min=direction  
                   except UnauthorizedMove:
                       pass                         
               return (gain_min,coup_min)
        
    def PlayTwoPlayers(self):             #Humain contre Humain
        global directions
        self.Show()    
        while not self.EndGame():
             self.AskPlayer()
             while True:
                 try:
                     direction = directions[input()]
                     self.PlayStroke(direction)
                     break
                 except:  #UnauthorizedMove (l.343) et KeyError (l.342)
                     print("Direction erronée. Choisissez-en une autre : ")
                     pass
             self.Show()
        print(self.Result())
        
    def PlayOnePlayer(self,profondeur):   #Humain contre I.A. 
        #PS : l'I.A. prend le nom du deuxième joueur en paramètre de Game
        global directions
        self.Show() 
        while not self.EndGame():
            if self.indice_courant==0:       #à l'humain de jouer
               self.AskPlayer()
               while True:
                   try:
                       direction = directions[input()]
                       self.PlayStroke(direction)
                       break
                   except:  #UnauthorizedMove (l.343) et KeyError (l.342)
                       print("Direction erronée. Choisissez-en une autre : ")
                       pass
               self.Show()
            else:                             #à l'IA de jouer
               print(self._Joueurs[1].nom + " est en train de réfléchir...")
               direction = self.MinMax(1,profondeur,True)[1]
               self.PlayStroke(direction)   
            self.Show()
        print(self.Result())
        
    def SeeAGame(self,profondeur):        #I.A. contre I.A. (spectateur)
        self.Show() 
        while not self.EndGame():
             print(self._Joueurs[self.indice_courant].nom \
                   + " est en train de réfléchir...")
             direction = self.MinMax(self.indice_courant,profondeur,True)[1]
             self.PlayStroke(direction)
             self.Show()
        print(self.Result())
 
        
#Implémentation du jeu en mode texte

'''
#4.1. DEFINITION DU JEU
G=Game(4,"Mario","Luigi",True) 
#le booléen indique si le joueur en 2ème paramètre de Game commence

#4.2  DEUX CHOIX POUR L'INITIALISATION DE LA GRILLE DE JEU: 
G.InitRandom()                     #soit aléatoire (dans valeurs_pieces) 
#G.LoadFromFile("grille55.csv")    #soit importée depuis un fichier

#4.3  TROIS CHOIX POUR LE MODE DE JEU :
#G.PlayTwoPlayers()  #Humain contre Humain
G.PlayOnePlayer(2)   #Humain contre I.A. (profondeur de l'I.A. en paramètre)  
#G.SeeAGame(2)       #I.A. contre I.A.  (profondeur des I.A. en paramètre)  
'''

#----------------
#Deux remarques concernant les tests sur des grilles importées :    
#1. Dans le cas où on importe la grille initiale depuis un fichier, la taille 
#du Plateau entrée dans le constructeur de Game n'a pas d'importance puisqu'
#elle sera réinitialisée automatiquement à celle de la grille du fichier
#2. Pour que l'IA fonctionne correctement sur une grille importée depuis un
#fichier, merci de s'assurer que le gain de chaque cellule ne dépasse pas la
#valeur maximale de valeurs_pieces. Si ce n'est pas le cas, veuillez ajouter 
#à la variable globale valeurs_pieces la valeur maximale des gains de la grille
#du fichier.

