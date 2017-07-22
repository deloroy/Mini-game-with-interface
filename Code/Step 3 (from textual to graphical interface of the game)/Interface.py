#Pour moi:
#c:\Users\Martine\Miniconda3\python.exe
#"C:\Users\Martine\Desktop\IMI\TDLOG\DELORO_TDLOG41\DELORO_TDLOG4\Interface.py"    
# -*- coding: utf-8 -*-                                                            

#DELORO Yonatan 

import Jeu
import sys
from PyQt4 import QtGui
 
#1. Menu du jeu 

class GameMenu(QtGui.QInputDialog):
    
    def __init__(self):
        super(GameMenu, self).__init__()    
        self.taille_grille=-1
        self.mode_jeu=-1    #1 si 1 joueur humain ou 2 si 2 joueurs humains
        (self.joueur1,self.joueur2)=("","")  #nom des 2 joueurs
        self.joueur1first=True  #le joueur 1 est-il le premier à jouer ?                        
        self.forceIA=-1         #profondeur de l'IA le cas échéant
        self.MainMenu()

    def MainMenu(self): 
        #Affiche un menu général où on choisit taille et mode de jeu 
        #(à 1 ou à 2 joueurs humains)

        #Choix de la taille de la grille :
        taille = 0 
        while (taille<3 or taille>9):  
            #le traitement d'une grille de taille paire est différent                             
            taille, ok1 = QtGui.QInputDialog.getInt(self, "Menu", 
            "Entrez la taille de la grille, entre 3 et 9 :")
        self.taille_grille=taille
        #si la taille de la grille est paire, on affiche un message indiquant
        #à l'utilsateur la correction qui va être effectuée par le programme
        if (self.taille_grille%2==0):
            self.InfoResetSize()  
        
        #Choix du mode de jeu (1 ou 2 joueurs) et appel du bon sous-menu :
        mode = -1
        while (mode!=1 and mode!=2):
            mode, ok2 = QtGui.QInputDialog.getInt(self, "Menu", "Entrez '1' " +
             "pour jouer seul contre l'ordinateur ou '2' pour jouer à 2.")
        self.mode_jeu=mode
        if self.mode_jeu==1:
            self.OnePlayerMenu()
        else:
            self.TwoPlayersMenu()
                       
    def OnePlayerMenu(self):
        #Affiche le sous-menu pour un jeu contre l'ordinateur (IA)
        
        #Choix du nom du joueur :
        ok1=False 
        #Ainsi l'utilisateur ne peut pas "sauter" la fenêtre avec "Cancel"
        while not ok1: 
            nom, ok1 = QtGui.QInputDialog.getText(self, "Menu 1J", 
              "Entrez le nom du joueur")
        self.joueur1=str(nom)
        self.joueur2="Computer IA"
    
        #Choix de la force de l'ordinateur (profondeur de l'IA) :
        profondeur = -1
        while (profondeur<1 or profondeur>4):
            profondeur, ok2 = QtGui.QInputDialog.getInt(self, "Menu 1J",
             "Entrez la force de l'IA (nombre de coups anticipés > 0, et < 5 "      
             + "pour un temps d'attente raisonnable)")            
        self.forceIA=profondeur
        
        #Choix du joueur qui joue en premier la première partie :
        reponse=-1
        while (reponse!=1 and reponse!=2):
            reponse, ok3 = QtGui.QInputDialog.getInt(self, "Menu 1J", 
              "Souhaitez-vous commencer la première partie ? 'Oui' -> 1," +
              " 'Non' -> 2 ?")
        if reponse==1:
           self.joueur1first=True
        else:
           self.joueur1first=False
        
            
    def TwoPlayersMenu(self):
        #Affiche le sous-menu pour un jeu à 2 joueurs humains
        
        #Choix des noms des joueurs :
        ok1=False
        while not ok1:  
            nom1, ok1 = QtGui.QInputDialog.getText(self, "Menu 2J", 
                "Entrez le nom du joueur 1")
        self.joueur1=str(nom1)
        ok2=False
        while not ok2:
            nom2, ok2 = QtGui.QInputDialog.getText(self, "Menu 2J", 
                "Entrez le nom du joueur 2")
        self.joueur1=str(nom1)
        self.joueur2=str(nom2)
            
        #Choix du joueur qui joue en premier la première partie :
        reponse = -1
        while (reponse!=1 and reponse!=2):
            reponse, ok3 = QtGui.QInputDialog.getInt(self, "Menu 2J", 
              "Qui commence la partie ? 'Joueur 1' -> 1, 'Joueur 2' -> 2 ?")
        if reponse==1:
           self.joueur1first=True
        else:
           self.joueur1first=False
            
    def InfoResetSize(self):
        #"Bulle d'information" à appeler si la grille est de taille paire
        anything, ok =  QtGui.QInputDialog.getText(self, "Information", "La"  
         + " taille de la grille doit être impaire. La taille que vous avez" 
         + " choisie a été incrémentée automatiquement de 1." + "\n"
         + "Veuillez ignorer la barre de dialogue et cliquer directement sur"
         + " Ok.")
              
#2. Interface graphique du jeu

class GameInterface(QtGui.QWidget):                                                      
    
    def __init__(self):
        super(GameInterface,self).__init__()
        
        #Lancement du menu pour définir les caractéristiques du jeu choisies
        #par le(s) joueur(s)
        self.menu=GameMenu() 

        #Définition du jeu
        self.jeu=Jeu.Game(self.menu.taille_grille,self.menu.joueur1, 
                          self.menu.joueur2,self.menu.joueur1first)                             
                
        #Initialisation de la grille de jeu
        self.jeu.InitRandom()                     #initialisation aléatoire

        #Création et initialisation de l'interface graphique du jeu
        #(on prend l'affichage en attribut de Interface car on en a besoin pour
        #récupérer les positions des boutons cliqués par les joueurs)
        self.affichage=QtGui.QGridLayout() 
        #(affichage est l'ensemble des éléments agencés sur l'interface) 
        self.setLayout(self.affichage)
        
        #Affichage de l'interface
        self.ShowGame() 
            
    def ShowGame(self):      
        #Affiche l'interface de jeu à un instant donné (grille, scores, nom
        #du joueur courant si jeu à 2 joueurs, résultat de la partie le cas
        #échant, avec possibilité de quitter le jeu et de rejouer une partie)

        self.move(0,0)  
        self.setWindowTitle('La grille')
        self.show()    #affichage   
        
        #booléen indiquant si le coup à venir est joué par un humain        
        a_humain_de_jouer=(self.menu.mode_jeu==2 or self.jeu.indice_courant==0)
        #2 cas : jeu à 2 Joueurs, ou à l'Humain de jouer dans un jeu contre IA
        
        #Ajout de la grille de jeu
        self.Add_Buttons_Grid(a_humain_de_jouer)
        #Ajout des scores des joueurs et de nom du joueur courant si jeu à 2J      
        self.Add_Buttons_Players()
        #Ajout de l'état de la partie : "partie en cours"/résultat final
        self.Add_Game_State()
        #Ajout des boutons "rejouer" cliquable uniquement à la fin d'une 
        #partie, et "quitter" tout le temps cliquable )
        self.Add_Button_PlayAgain()
        self.Add_Button_Exit()

        #Appel du coup de l'IA si la partie n'est pas finie, 
        #si c'est le mode de jeu en question (1 joueur) et si c'est à son tour 
        #de jouer
        if ((not self.jeu.EndGame()) and (not a_humain_de_jouer)):
            self.Play_Stroke_IA()     
            
    def Add_Buttons_Grid(self, a_humain_de_jouer):
        #Ajoute la grille à l'interface, en configurant l'état
        #de chaque bouton (case de la grille) comme actif (cliquable par le
        #joueur à l'instant considéré) ou non, et qui actualise et affiche
        #la nouvelle grille si un bouton est cliqué par le joueur
        #le paramètre a_humain_de_jouer est un booléen indiquant si c'est à un 
        #joueur humain de jouer à l'instant considéré
        
        #Cases actives de la grille (cliquables par le joueur) :
        cases_actives=[]
        if a_humain_de_jouer:
            for direction in Jeu.directions.values():
                try:
                    cases_actives.append(self.jeu.NewPosition(direction))
                except Jeu.UnauthorizedMove:
                    pass
            
        #Ajout de la grille à l'interface :
        for i in range(self.jeu._Plateau.taille):
            for j in range(self.jeu._Plateau.taille):
                gain=self.jeu._Plateau[i,j]
                nom=str(gain)+(3-len(str(gain)))*" " + " " 
                bouton=QtGui.QPushButton(nom)
                self.affichage.addWidget(bouton,*(i,j))
                #configuration des états des cases (actif/non) :
                if (i,j) in cases_actives:
                    #si la case est cliquable, on connecte le signal "clicked"
                    #à la methode qui va recueillir le coup du joueur et 
                    #afficher la nouvelle grille actualisée
                    bouton.clicked.connect(self.Collect_Stroke_Player)       
                else:
                    bouton.setEnabled(False)   
    
    def Collect_Stroke_Player(self):
        #Calcule et affiche le nouvel état de la partie après déplacement du 
        #personnage sur la case cliquée par le joueur
        
        #Récupération de la position de la case cliquée dans la grille :
        index_bouton=self.affichage.indexOf(self.sender())
        #Calcul de la direction de déplacement du personnage par différence
        #entre la position désirée par le joueur et son ancienne position :
        (x_new,y_new) = self.affichage.getItemPosition(index_bouton)[0:2]
        direction = (x_new-self.jeu._Personnage[0],y_new-self.jeu._Personnage[1])
        self.jeu.PlayStroke(direction)   #Actualisation de la grille
        self.ShowGame()                  #Affichage du nouvel état de la partie
        
    def Add_Buttons_Players(self):
        #Ajoute les scores des joueurs à l'interface, ainsi que le nom du 
        #joueur courant (dont c'est le tour) si le mode de jeu est à 2 joueurs
        Taille=self.jeu._Plateau.taille
        
        #Ajout des scores des joueurs à l'interface :
        for (i,joueur) in enumerate(self.jeu._Joueurs):
            bouton_joueur=QtGui.QPushButton(joueur.nom + " : " + str(joueur.score))
            self.affichage.addWidget(bouton_joueur,*(Taille,i))
            bouton_joueur.setEnabled(False)

        #Ajout du nom du joueur courant pour un jeu à 2 joueurs humains :
        if self.menu.mode_jeu==2:
           if not self.jeu.EndGame():
               info = "A "+ self.jeu._Joueurs[self.jeu.indice_courant].nom \
                       + " de jouer" 
           else:
               info = "Partie finie"
           bouton_info=QtGui.QPushButton(info)
           self.affichage.addWidget(bouton_info,*(Taille,3))
           bouton_info.setEnabled(False)
    
    def Add_Game_State(self):
        #Ajoute de l'état de la partie ("partie en cours"/résultat final) à 
        #l'interface
        message=""
        if self.jeu.EndGame():
            message=self.jeu.Result()
        else:
            message="Partie en cours"
        bouton_message=QtGui.QPushButton(message)
        Taille=self.jeu._Plateau.taille
        self.affichage.addWidget(bouton_message,*(Taille,4))
        bouton_message.setEnabled(False)

    def Play_Stroke_IA(self):
        #Actualise la grille et appelle son affichage suite au coup joué par
        #l'intelligence artificielle
        direction = self.jeu.MinMax(1,self.menu.forceIA,True)[1]                     
        self.jeu.PlayStroke(direction)
        self.ShowGame() 
        
    def Add_Button_PlayAgain(self):
        #Ajoute un bouton "Rejouer" à l'interface qui n'est cliquable qu'à
        #la fin d'une partie
        bouton_rejouer=QtGui.QPushButton("Rejouer")
        Taille=self.jeu._Plateau.taille
        self.affichage.addWidget(bouton_rejouer,*(Taille,Taille+2))
        if self.jeu.EndGame():
           #si le jeu est fini, on connecte le signal "clicked" sur "rejouer"              
           #à la methode qui va permettre l'affichage d'une nouvelle grille
           #à jouer
            bouton_rejouer.clicked.connect(self.PlayAgain) 
        else:        
            bouton_rejouer.setEnabled(False)

    def PlayAgain(self):
        #Lance une nouvelle partie avec les mêmes joueurs, la même taille de
        #grille et l'ordre de jeu inversé (joueur 2 commence si joueur 1 a 
        #commencé la dernière partie)
        self.menu.joueur1first=not self.menu.joueur1first
        self.jeu=Jeu.Game(self.menu.taille_grille,self.menu.joueur1,
                          self.menu.joueur2,self.menu.joueur1first)                             
        self.jeu.InitRandom()                     #initialisation aléatoire
        self.ShowGame()
    
    def Add_Button_Exit(self):
        #Ajoute un bouton "Quitter" à l'interface cliquable à tout moment
        #(Ceci est un choix)
        bouton_quitter=QtGui.QPushButton("Quitter")
        Taille=self.jeu._Plateau.taille
        self.affichage.addWidget(bouton_quitter,*(Taille,Taille+3))
        bouton_quitter.clicked.connect(lambda signal: self.close()) 

        
#3. Implémentation du jeu avec menu et interface graphique

def Play():
    app = QtGui.QApplication(sys.argv)
    GameInterface()                                                                                  
    sys.exit(app.exec_())

Play()

