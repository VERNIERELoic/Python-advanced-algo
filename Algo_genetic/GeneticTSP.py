from cmath import sqrt
from curses.ascii import NUL
from fileinput import filename
import os
import random as rand
import csv
from cv2 import sqrBoxFilter
from tenacity import t


class PVC_Genetique:

    def __init__(self, list_villes, taille_population=40, nbr_generation=100):
        self.list_villes = list_villes
        self.taille_population = taille_population
        self.nbr_generation = nbr_generation
        self.elitisme = True
        self.mut_proba = 0.3

    def croiser(self, parent1, parent2):
        enfant = []
        for i in range(len(parent1//2)):
            tmp1 = parent1[i]
            tmp2 = parent2[len(parent2)-i]

        enfant.append(tmp1 + tmp2)

        if len(set(enfant)) != len(enfant):
            for i in range(len(set(enfant))):
                if i not in set(enfant):
                    set(enfant).add(i)
        # set(enfant).add(set(enfant).difference(parent1))
        return enfant

    # Mutation : on prend un item a un index aleatoire, on le pop et insert a la fin
    def muter(self, trajet):
        mutation = trajet.pop(rand.randint(0, len(self.list_villes)-2))
        trajet.insert(mutation)
        trajet.calc_longueur()
        return mutation

    def selectionner(self, population):
        # Utilisation des operateur magique
        sorted(population.trajet)[:len(population.trajet)//2]

    def evoluer(self, population):
        selection = population.selectionner(population)
        changed = []
        for i in range(len(selection)):
            if rand.randint(0, 100) < self.mut_proba*100:
                changed.append(selection.croiser(
                    population[i], population[i+1]))
            else:
                changed.append(self.muter(selection.trajet[i]))

        return changed

    def executer(self):
        actu_meilleur = 0
        p = Population()
        p.initialiser(len(p.list_trajet), self.list_villes)
        actu_meilleur = p.list_trajet.meilleur()
        for i in range(self.nbr_generation):
            self.evoluer(p)
            if actu_meilleur > p.list_trajet[i].meilleur():
                actu_meilleur = p.list_trajet[i].meilleur()

    def clear_term(self):
        os.system('cls' if os.name == 'nt' else 'clear')


class Ville:
    def __init__(self, nom, x, y):
        self.nom = nom
        self.x = x
        self.y = y

    def distance_vers(self, autre_ville):
        return sqrt(self.x - autre_ville.x)**2 + sqrt(self.y - autre_ville.y)**2

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
    def __init__(self, list_ville=None):
        self.longueur = 0
        if list_ville is not None:
            self.villes = list_ville
            self.trajet = []
            for i in range(len(self.list)):
                self.trajet.append(self.villes[rand(0, len(self.villes))])

    def calc_longueur(self):
        self.longueur = 0
        for i in range(len(self.villes) - 1):
            self.longueur += self.villes[i].distance_vers(self.villes[i+1])

    def est_valide(self):
        for elem in self.villes:
            if self.villes.count(elem) > 1:
                return True
            return False

    def __str__(self):
        return str(self.trajet_rand)

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

    def ajouter(self, trajet):
        self.list_trajet.append(trajet)

    def meilleur(self):
        for i in range(len(self.list_trajet)):
            if self.list_trajet[i.longueur] < min:
                min = self.list_trajet[i.longueur]

        return min

    def __str__(self):
        return str(self.list_trajet)


def main():
    villes = generer_villes()
    pvc = PVC_Genetique()
    pvc.executer()
    # print(villes[2])
    return


if __name__ == "__main__":
    main()
