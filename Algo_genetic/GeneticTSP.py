from math import sqrt
from curses.ascii import NUL
from fileinput import filename
import os
import random as rand
import csv
from tenacity import t
import copy
import GeneticTSPGui


class PVC_Genetique:

    def __init__(self, list_villes, taille_population=40, nbr_generation=100):
        self.list_villes = list_villes
        self.taille_population = taille_population
        self.nbr_generation = nbr_generation
        self.elitisme = True
        self.gui = GeneticTSPGui(self.list_villes)
        self.mut_proba = 0.3

    def croiser(self, parent1, parent2):
        m = len(parent1.villes) // 2
        new_trajet = parent1.villes[:m] + parent2.villes[m:]
        missing = []
        if (len(set(new_trajet)) != new_trajet) and len(new_trajet) != len(self.list_villes):
            for ville in range(len(self.list_villes)):
                if ville.nom not in set(new_trajet).keys():
                    missing.append(ville)
        enfant = Trajet(new_trajet + missing)
        enfant.calc_longueur()
        return enfant

    # Mutation : on prend un item a un index aleatoire, on le pop et insert a la fin
    def muter(self, trajet):
        mutation = trajet.villes.pop(rand.randint(0, len(self.list_villes)-2))
        trajet.villes.append(mutation)
        trajet.calc_longueur()
        return trajet

    def selectionner(self, population):
        # Utilisation des operateur magique
        return sorted(population.list_trajet)[:len(population.list_trajet)//2]

    def evoluer(self, population):
        selection = self.selectionner(population)
        selection_cp = selection.copy()
        for i in range(len(selection)):
            if rand.randint(0, 100) < self.mut_proba*100:
                population.ajouter(self.muter(selection[i]))
            else:
                if len(selection_cp) != (i+1):
                    population.ajouter(self.croiser(
                        selection_cp[i], selection_cp[i+1]))
                else:
                    population.ajouter(self.muter(selection_cp[i]))

        return population

    def executer(self, afficher):
        population = Population()
        population.initialiser(self.taille_population, self.list_villes)
        global_meilleur = population.meilleur()
        for i in range(self.nbr_generation):
            population = self.evoluer(population)
            actu_meilleur = population.meilleur()
            print("global_meilleur : ", global_meilleur)
            if actu_meilleur < global_meilleur:
                global_meilleur = actu_meilleur
            print("actu_meilleur : ", actu_meilleur)

            if afficher == True:
                self.gui.afficher(global_meilleur, actu_meilleur)
        self.gui.window.mainloop()

    def clear_term(self):
        os.system('cls' if os.name == 'nt' else 'clear')


class Ville:
    def __init__(self, nom, x, y):
        self.nom = nom
        self.x = x
        self.y = y

    def distance_vers(self, autre_ville):
        return sqrt((self.x - autre_ville.x)**2 + (self.y - autre_ville.y)**2)

    def __str__(self):
        return str(self.nom)


def generer_villes(nb_ville=20):
    list_ville = []
    for i in range(nb_ville):
        x = rand.randint(0, 300)
        y = rand.randint(0, 300)
        list_ville.append(Ville(i, x, y))
    return list_ville


def lire_csv(file_name):
    with open(file_name) as file_obj:
        reader_obj = csv.reader(file_obj)
        for row in reader_obj:
            print(row)


class Trajet:
    def __init__(self, list_ville):
        self.longueur = 0
        if list_ville is not None:
            self.villes = list_ville
            self.trajet = list_ville.copy()
            rand.shuffle(self.trajet)

    def calc_longueur(self):
        self.longueur = 0
        for i in range(len(self.villes) - 1):
            # print(self.villes[i].distance_vers(self.villes[i+1]))
            self.longueur += self.villes[i].distance_vers(self.villes[i+1])

    def est_valide(self):
        for elem in self.villes:
            if self.villes.count(elem) > 1:
                return False
            return True

    def __str__(self):
        return "Trajet:" + str([str(v) for v in self.trajet])

    # Utilisation des operateurs magique pour le selectionner
    def __lt__(self, other):
        return self.longueur < other.longueur

    def __gt__(self, other):
        return self.longueur > other.longueur

    def __eq__(self, other):
        return self.longueur == other.longueur


class Population:
    def __init__(self):
        self.list_trajet = []

    def initialiser(self, taille, list_villes):
        for i in range(taille):
            t = Trajet(list_villes)
            t.calc_longueur()
            self.list_trajet.append(t)
        # print(self.list_trajet)

    def ajouter(self, trajet):
        self.list_trajet.append(trajet)

    def meilleur(self):
        min = self.list_trajet[0]
        print("min", self.list_trajet[0].longueur)
        for i in range(len(self.list_trajet)):
            if self.list_trajet[i].longueur < min.longueur:
                min = self.list_trajet[i]
        return min

    def __str__(self):
        return str(self.list_trajet)


def main():
    villes = generer_villes()
    pvc = PVC_Genetique(villes)
    pvc.executer(True)
    return


if __name__ == "__main__":
    main()
