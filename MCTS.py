from abc import ABC, abstractmethod
from collections import defaultdict
from copy import copy
import math
import numpy as np


class Noeud(ABC):
    """
    Noeud de l'arbre MCTS (représente un état de la partie)
    """

    @abstractmethod
    def generer_noeuds_fils(self):
        "Ensemble des noeuds successeurs possibles du noeud courant"
        return set()

    @abstractmethod
    def generer_un_noeud_fils_aleatoire(self):
        "Générer un noeud successeur aléatoirement"
        return None

    @abstractmethod
    def est_terminal(self):
        return True

    @abstractmethod
    def resultat_partie(self):
        "Résultat de la partie"
        return 0

    @abstractmethod
    def __hash__(self):
        "Pour s'assurer que les noeuds soit hashable"
        return 123456789

    @abstractmethod
    def __eq__(n1, n2):
        "Pour s'assurer que les noeuds soient comparables"
        return True


class Arbre_MCTS:
    def __init__(self, coeff_uct=1):
        self.nb_victoires = defaultdict(int)  # nombre de victore du noeud
        self.nb_visites = defaultdict(int)  # nombre de visite du noeud
        self.noeuds_fils = dict()  # noeuds fils du noeud
        self.coeff_uct = coeff_uct # paramètre de l'algorithme UCT

    def choisir_action(self, noeud):
        "Choix du meilleur noeud successeur pour le prochain coup"

        if noeud not in self.noeuds_fils:
            return noeud.generer_un_noeud_fils_aleatoire()

        def nb_moyen_victoires(n):

            # Si le noeud n'a jamais été joué, on lui 
            # attribue un score -inf
            if self.nb_visites[n] == 0:
                return float("-inf") 
                
            return self.nb_victoires[n] / self.nb_visites[n]

        return max(self.noeuds_fils[noeud], key=nb_moyen_victoires)


    ##### UCT

    def simulation_partie_complete(self, noeud):
        "Simuler une partie complète (jusqu'à un état terminal)"
        chemin = self.selection(noeud)
        feuille = chemin[-1]
        self.expansion(feuille)
        resultat_partie = self.simuler_partie(feuille)
        self.retropropagation(chemin, resultat_partie)

    def selection(self, noeud):
        "Phase de sélection: Descente de l'arbre et choisir un noeud successeur selon une stratégie"
        chemin = []
        while True:
            chemin.append(noeud)
            if noeud not in self.noeuds_fils or not self.noeuds_fils[noeud]:
                return chemin
            noeud_non_explore = self.noeuds_fils[noeud] - self.noeuds_fils.keys()


            if noeud_non_explore:
                n = noeud_non_explore.pop()
                chemin.append(n)
                return chemin                     

            "Sélection d'un noeud fils avec la stratégie UCT"
            noeud = self.echantillonnage_uct(noeud)     

    def expansion(self, noeud):
        "Phase d'expansion : générer un nouveau noeud fils du noeud courant"
        if noeud in self.noeuds_fils:
            return  # already expanded
        self.noeuds_fils[noeud] = noeud.generer_noeuds_fils()

    def simuler_partie(self, noeud):
        "Simuler une partie aléatoire complète à partir du noeud courant et récupérer la résultat"
        invert_reward = True
        while True:
            if noeud.est_terminal():
                resultat_partie = noeud.resultat_partie()
                return 1 - resultat_partie if invert_reward else resultat_partie
            noeud = noeud.generer_un_noeud_fils_aleatoire()
            invert_reward = not invert_reward

    def retropropagation(self, chemin, resultat_partie):
        "Phase de retropropagation : mise à jour les statistiques des noeuds antécédents"
        for noeud in reversed(chemin):
            self.nb_visites[noeud] += 1
            self.nb_victoires[noeud] += resultat_partie
            resultat_partie = 1 - resultat_partie  # 1 for me is 0 for my enemy, and vice versa

    def echantillonnage_uct(self, noeud):
        "Sélection d'un noeud fils avec la stratégie UCT"
        # Tous les noeuds fils du noeud courant doivent être tous passés par 
        # la phase d'exansion
        assert all(n in self.noeuds_fils for n in self.noeuds_fils[noeud])

        log_ = math.log(self.nb_visites[noeud])

        def uct(n):
            return self.nb_victoires[n] / self.nb_visites[n] + self.coeff_uct * math.sqrt(
                log_ / self.nb_visites[n]
            )

        return max(self.noeuds_fils[noeud], key=uct)
    
    




    # #### RAVE
    # def rave(self,noeud, played):
    #     pass

    # def best_move_rave(self,noeud, budget):
    #     for i in range(budget):
    #         b1 = copy.deepcopy(noeud)
    #         res = self.rave(b1, [])
        
 

    




