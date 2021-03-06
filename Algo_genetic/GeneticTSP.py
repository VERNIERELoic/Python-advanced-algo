from math import sqrt
from curses.ascii import NUL
from fileinput import filename
import os
import random as rand
import csv
import copy
from GeneticTSPGui import PVC_Genetique_GUI


class PVC_Genetique:

    def __init__(self, list_villes, taille_population=15, nbr_generation=100):
        self.list_villes = list_villes
        self.taille_population = taille_population
        self.nbr_generation = nbr_generation
        self.elitisme = True
        self.gui = PVC_Genetique_GUI(self.list_villes)
        self.mut_proba = 0.80  # j'ai augmenté la probalilité de mutation car meilleurs resultats

    # Si des doublons, on passe la list en set qui supprime automatiquement les doublons
    # On test si la ville est presente en bouclant sur l'enfant puis on ajoute a la list des villes manquantes
    # enfant prend alors une nouvelle list de type Trajet (enfant + villes manquantes)
    def croiser(self, parent1, parent2):
        villes1 = parent1.villes
        villes2 = parent2.villes
        moitier = len(villes1)//2
        enfant = Trajet(villes1[:moitier] + villes2[moitier:])
        if not enfant.est_valide():
            enfant.villes = set(enfant.villes)
            villes_manquantes = []
            for ville in self.list_villes:
                if ville.nom not in [boucle_ville.nom for boucle_ville in enfant.villes]:
                    villes_manquantes.append(ville)
            enfant = Trajet(list(enfant.villes) + villes_manquantes)
        enfant.calc_longueur() #On pense a mettre a jour la longueur
        return enfant

    # Mutation : on prend un item a un index aleatoire, on le pop et insert a la fin
    def muter(self, trajet):
        mutation = trajet.villes.pop(rand.randint(0, len(self.list_villes)-2))
        trajet.villes.append(mutation)
        trajet.calc_longueur() #On pense a mettre a jour la longueur
        return trajet

    def selectionner(self, population):
        # Utilisation des operateur magique poour comparer les objects (voir classe Trajet)
        # On selection les 10 meilleurs
        return sorted(population.list_trajet[::])[::10]

    # Si le rand generé est < à la proba, alors on mute sinon on test si la selection esy differente
    # de la selection + 1 et si oui alors on croise les population
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
        # insère dans l'objet composé des copies des objets trouvés dans l'objet original.
        global_meilleur = copy.deepcopy(population.meilleur())
        # Boucle autant de fois que de generation...
        for i in range(self.nbr_generation):
            population = self.evoluer(population)
            print(population.meilleur().longueur, global_meilleur.longueur)
            actu_meilleur = population.meilleur()
            if actu_meilleur < global_meilleur:
                global_meilleur = copy.deepcopy(actu_meilleur)

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
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        villes = []
        for row in reader:
            villes.append(Ville(int(row[0]), int(row[1]), int(row[2])))
        return villes


class Trajet:
    def __init__(self, list_ville):
        self.longueur = 0
        if list_ville is not None:
            self.villes = list_ville
            self.trajet = list_ville.copy()
            rand.shuffle(self.trajet)  # Reorganise l'ordre des items

    def calc_longueur(self):
        self.longueur = 0
        for i in range(len(self.villes) - 1):
            print(self.villes[i].distance_vers(self.villes[i+1]))
            self.longueur += self.villes[i].distance_vers(self.villes[i+1])

    # test si ville present + de 1 fois
    def est_valide(self):
        for elem in self.villes:
            if self.villes.count(elem) > 1:
                return False
        return True

    def __str__(self):
        return "Trajet:" + str([str(v) for v in self.trajet])

    # Utilisation des operateurs magique pour le selectionner et pourvoir comparer les objects entre eux
    # equal, lower than, greater than.
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
        trajet.calc_longueur()
        self.list_trajet.append(trajet)

    def meilleur(self):
        min = self.list_trajet[0]
        for i in range(len(self.list_trajet)):
            if self.list_trajet[i].longueur < min.longueur:
                min = self.list_trajet[i]
                # print(min)
        return min

    def __str__(self):
        return str(self.list_trajet)


def main():
    villes = lire_csv('30.csv')
    pvc = PVC_Genetique(villes)
    pvc.executer(True)
    return


if __name__ == "__main__":
    main()
