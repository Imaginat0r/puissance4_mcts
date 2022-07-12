from ast import Raise
import numpy as np
import pygame
import sys
import math
from tkinter import *
from tkinter import messagebox
from datetime import datetime 
from Popup import PopUp
from MCTS import Arbre_MCTS,Noeud
from collections import namedtuple
from random import choice

def inserer_jeton(plateau, ligne, col, joueur):
	"Placer un jeton dans une colonne disponible"
	plateau[ligne][col] = joueur

def colonne_jouable(plateau, col):
	"Détermine si une colonne est disponible"
	return plateau[NB_LIGNES-1][col] == 0

def prochaine_ligne_dispo(plateau, col):
	for r in range(NB_LIGNES):
		if plateau[r][col] == 0:
			return r

def colonnes_valides(plateau):
	emplacements_valides = []
	for col in range(NB_COLS):
		if colonne_jouable(plateau, col):
			emplacements_valides.append(col)
	return emplacements_valides

def affichier_plateau(trame,plateau):
	"Mise à jour et affichage du plateau avec pygame"
	for c in range(NB_COLS):
		for r in range(NB_LIGNES):
			pygame.draw.rect(trame, couleurs.get("BLEU"), (c*TAILLE_BLOC, r*TAILLE_BLOC, TAILLE_BLOC, TAILLE_BLOC))
			pygame.draw.circle(trame, couleurs.get("BLANC"), (int(c*TAILLE_BLOC+TAILLE_BLOC/2), int(r*TAILLE_BLOC+TAILLE_BLOC/2)), RAYON)
	
	for c in range(NB_COLS):
		for r in range(NB_LIGNES):		
			if plateau[r][c] == JOUEUR_1:
				pygame.draw.circle(trame, couleurs.get("ROUGE"), (int(c*TAILLE_BLOC+TAILLE_BLOC/2), hauteur-int(r*TAILLE_BLOC+TAILLE_BLOC/2)), RAYON)
			elif plateau[r][c] == JOUEUR_2: 
				pygame.draw.circle(trame, couleurs.get("JAUNE"), (int(c*TAILLE_BLOC+TAILLE_BLOC/2), hauteur-int(r*TAILLE_BLOC+TAILLE_BLOC/2)), RAYON)
	pygame.display.update()

def conversion_etat(matrice):
	"""Conversion de la grille de jeu (numpy array) en tuple hashable"""
	return tuple(matrice.flatten())

def conversion_matrice(etat):
	"""Conversion d"un tuple hashable en grille de jeu (numpy array)"""
	plateau = np.asarray(etat)
	return plateau.reshape(NB_LIGNES,NB_COLS)

def choix_mode_jeu():
	"""Affichage d'une fenêtre pour la sélection du mode de jeu"""
	popup = PopUp("Mode de jeu")	
	return popup.choix

def recherche_gagnant(etat):
	"Retourne le joueur gagnant, None si pas de gagnant"

	if recherche_coup_gagnant(etat, JOUEUR_1):
		return JOUEUR_1
	
	if recherche_coup_gagnant(etat, JOUEUR_2):
		return JOUEUR_2
	
	return None

def recherche_coup_gagnant(plateau, joueur):
	for c in range(NB_COLS-3):
		for r in range(NB_LIGNES):
			if plateau[r][c] == joueur and plateau[r][c+1] == joueur and plateau[r][c+2] == joueur and plateau[r][c+3] == joueur:
				return True

	for c in range(NB_COLS):
		for r in range(NB_LIGNES-3):
			if plateau[r][c] == joueur and plateau[r+1][c] == joueur and plateau[r+2][c] == joueur and plateau[r+3][c] == joueur:
				return True

	for c in range(NB_COLS-3):
		for r in range(NB_LIGNES-3):
			if plateau[r][c] == joueur and plateau[r+1][c+1] == joueur and plateau[r+2][c+2] == joueur and plateau[r+3][c+3] == joueur:
				return True

	for c in range(NB_COLS-3):
		for r in range(3, NB_LIGNES):
			if plateau[r][c] == joueur and plateau[r-1][c+1] == joueur and plateau[r-2][c+2] == joueur and plateau[r-3][c+3] == joueur:
				return True



structure = namedtuple("Puissance4_Board", "etat joueur_actuel gagnant est_une_feuille")

class Puissance4_Board(structure,Noeud):
	"""Plateau de jeu Puissance 4"""
	def generer_noeuds_fils(plateau):

		if plateau.est_une_feuille: 
			return set()

		etat = plateau.etat
		plateau_matrice = conversion_matrice(etat)

		return {
			plateau.jouer_coup(col) for col in range(NB_COLS) if colonne_jouable(plateau_matrice,col)
		}

	def generer_un_noeud_fils_aleatoire(plateau):
		if plateau.est_une_feuille:
			return None  

		etat = plateau.etat
		plateau_matrice = conversion_matrice(etat)

		colonnes_dispos = colonnes_valides(plateau_matrice)

		return plateau.jouer_coup(choice(colonnes_dispos))

	def resultat_partie(plateau):
		if plateau.joueur_actuel == JOUEUR_1:
			adversaire = JOUEUR_2
		else:
			adversaire = JOUEUR_1	

		if plateau.gagnant is plateau.joueur_actuel:
			return 1 
		if plateau.gagnant is adversaire:
			return 0 
		if plateau.gagnant is None:
			return 0.5 


	def est_terminal(plateau):
		return plateau.est_une_feuille

	def jouer_coup(plateau, col):

		plateau_matrice = conversion_matrice(plateau.etat)
		joueur_actuel = plateau.joueur_actuel
		
		ligne = prochaine_ligne_dispo(plateau_matrice, col)
		inserer_jeton(plateau_matrice, ligne, col, joueur_actuel)

		# Changement du joueur 
		if joueur_actuel == JOUEUR_1:
			joueur_actuel = JOUEUR_2
		else:
			joueur_actuel = JOUEUR_1	

		gagnant = recherche_gagnant(plateau_matrice)
		colonnes_dispos = colonnes_valides(plateau_matrice)
		est_terminal = (gagnant is not None) or (len(colonnes_dispos) == 0)

		return Puissance4_Board(conversion_etat(plateau_matrice), joueur_actuel, gagnant, est_terminal)


couleurs = {
	"BLEU" : (25,100,255),
	"BLANC" : (255,255,225),
	"NOIR" : (0,0,0),
	"ROUGE" : (255,0,0),
	"JAUNE" : (255,255,0)	
}

VIDE = 0
JOUEUR_1 = 1
JOUEUR_2 = 2

# GRILLE DE JEU
NB_LIGNES = 6
NB_COLS = 7
TAILLE_BLOC = 120
RAYON = int(TAILLE_BLOC/2 - 5)
largeur = NB_COLS * TAILLE_BLOC
hauteur = NB_LIGNES * TAILLE_BLOC


if __name__ == "__main__":
	plateau_matrice = np.zeros((NB_LIGNES,NB_COLS))

	pygame.init()
	trame = pygame.display.set_mode((largeur, hauteur))
	pygame.display.update()
	police = pygame.font.SysFont("monospace", 75)
	affichier_plateau(trame,plateau_matrice)


	# BUDGET ###########################################
	# 0 pour nombre de simulation
	# 1 pour temps maximum autorisé
	mode_budget = 1

	# Nombre de playouts avant de choisir le meilleur coup
	n_simu = 20

	# Temps de réponse maximum autorisé
	t_SIMU = 0.5 #s

	# Coefficient UCT
	coef_uct = 1

	#### CHOIX DU MODE DE JEU ##########################
	mode_jeu = choix_mode_jeu()
	print(f"Le mode de jeu choisi est : {mode_jeu}")

	arbre = Arbre_MCTS(coeff_uct=coef_uct)
	plateau = Puissance4_Board(etat=conversion_etat(plateau_matrice), joueur_actuel=JOUEUR_1, gagnant=None, est_une_feuille=False)
	
	turn = True

	while True:	

		# On vérifie si la partie est finie
		if plateau.est_une_feuille:
			break
		
		if turn:
			if mode_jeu == 1:
				plateau_matrice = conversion_matrice(plateau.etat)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()

					pygame.display.update()

					if event.type == pygame.MOUSEBUTTONDOWN:
						pygame.draw.rect(trame, couleurs.get("NOIR"), (0,0, largeur, TAILLE_BLOC))
						posx = event.pos[0]
						col = int(math.floor(posx/TAILLE_BLOC))

						if colonne_jouable(plateau_matrice, col):
							plateau = plateau.jouer_coup(col)
							turn = not turn
		
			elif mode_jeu == 2:
				if mode_budget == 0:
					for _ in range(n_simu):
						arbre.simulation_partie_complete(plateau)
				elif mode_budget == 1:
					t1 = datetime.now()
					while (datetime.now()-t1).seconds <= t_SIMU:
						arbre.simulation_partie_complete(plateau)
				else:
					raise("Stratégie de budget inconnue")

				turn = not turn

			else:
				Raise("Mode de jeu invalide !")
			
		else:
			if mode_budget == 0:
				# Stratégie nombre de simus
				for _ in range(n_simu):
					arbre.simulation_partie_complete(plateau)
			elif mode_budget == 1:
				# Stratégie Temps
				t1 = datetime.now()
				while (datetime.now()-t1).seconds <= t_SIMU:
					arbre.simulation_partie_complete(plateau)
			else:
				raise("Stratégie de budget inconnue")

			plateau = arbre.choisir_action(plateau)
			turn = not turn


		affichier_plateau(trame,conversion_matrice(plateau.etat))
		
		pygame.time.wait(50)

	affichier_plateau(trame,conversion_matrice(plateau.etat))

	Tk().wm_withdraw() 
	messagebox.showinfo("Résultat du match",f'FIN DE PARTIE \n Le joueur gagnant est : JOUEUR {plateau.gagnant}')