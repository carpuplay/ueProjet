import os






# Description: Main file for the game
### VARIABLES

plateau_debut = [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [2, 2, 2, 2],
    [2, 2, 2, 2],
]

plateau_milieu = [
    [1, 1, 0, 0],
    [1, 1, 1, 1],
    [2, 2, 2, 2],
    [2, 2, 2, 2],
]

plateau_fin = [
    [1, 1, 0, 0],
    [1, 1, 0, 0],
    [2, 0, 0, 0],
    [0, 2, 0, 0],
]


LIGNES = {0: "A", 1: "B", 2: "C", 3: "D"}
PIONS = {0: " ", 1: "●", 2: "○"}

pions_noirs = 8
pions_blancs = 8

def choisir_plateau():       #bon
    plateau_dico = { '1': plateau_debut, '2': plateau_milieu, '3': plateau_fin }
    while True:
        choix = input("Entrez votre choix (1, 2 ou 3) : ")
        if choix in plateau_dico:
            return plateau_dico.get(choix)
        else:
            print("Choix invalide. Veuillez entrer 1, 2 ou 3.")


def afficher_plateau(plateau):   #bon
    # Couleurs pour les pions
    couleur_pion = {1: '\033[91m', 2: '\033[96m', 0: '\033[0m'}
    print('     1   2   3   4')
    for ligne_index, ligne in enumerate(plateau):
        print(f" {LIGNES[ligne_index]} | ", end='')
        for case in ligne:
            print(couleur_pion[case] + PIONS[case] + '\033[0m' + ' | ', end='')
        print()


def demander_mouvement(joueur):   #bon
    while True:
        deplacement = input(f"\033[1mJoueur {joueur}, entrez votre deplacement (ex: A1 B2) : \033[0m")
        if valider_format_saisie(deplacement):
            case1, case2 = deplacement.split()
            if est_au_bon_format(case1, case2):
                return (case1, case2)
            else:
                print("\033[91mdeplacement invalide. Veuillez entrer deux cases valides.\033[0m")
        else:
            print("\033[91mdeplacement invalide. Veuillez entrer deux cases séparées par un espace.\033[0m")

def valider_format_saisie(deplacement):
    return len(deplacement) == 5 and deplacement[2] == " "

def est_au_bon_format(case1, case2):
  num_valide = ["1", "2", "3", "4"]
  lettre_valide = "ABCD"
  return case1[0] in lettre_valide and case1[1] in num_valide and case2[0] in lettre_valide and case2[1] in num_valide

def deplacer_pion(plateau, case1, case2, joueur):   #bon
    # Convertir les cases en index
    case1_index = (ord(case1[0].lower()) - ord('a'), int(case1[1])-1)
    case2_index = (ord(case2[0].lower()) - ord('a'), int(case2[1])-1)

    # Vérifier si le déplacement est valide
    if plateau[case1_index[0]][case1_index[1]] == joueur:
        if abs(case1_index[0] - case2_index[0]) == 2 or abs(case1_index[1] - case2_index[1]) == 2:
            # Vérifier si le pion à sauter est un pion adverse
            pion_a_sauter_index = ((case1_index[0] + case2_index[0]) // 2, (case1_index[1] + case2_index[1]) // 2)
            if plateau[pion_a_sauter_index[0]][pion_a_sauter_index[1]] == joueur and plateau[case2_index[0]][case2_index[1]] != 0 and plateau[case2_index[0]][case2_index[1]] != joueur:
                plateau[case1_index[0]][case1_index[1]] = 0
                plateau[case2_index[0]][case2_index[1]] = joueur
                return True
        # Vérifier si le déplacement est un déplacement normal
        elif (case1_index[0] == case2_index[0] and abs(case1_index[1] - case2_index[1]) == 1) or (case1_index[1] == case2_index[1] and abs(case1_index[0] - case2_index[0]) == 1):
            if plateau[case2_index[0]][case2_index[1]] == 0:
                plateau[case1_index[0]][case1_index[1]] = 0
                plateau[case2_index[0]][case2_index[1]] = joueur
                return True
    return False


def verifier_victoire(plateau):   #bon
    global pions_noirs, pions_blancs
    pions_noirs = 0
    pions_blancs = 0
    for ligne in plateau:
        for case in ligne:
            if case == 1:
                pions_noirs += 1
            elif case == 2:
                pions_blancs += 1
    if pions_noirs == 1:
        return 2
    elif pions_blancs == 1:
        return 1
    else:
        if not peut_deplacer(plateau, 1) and not peut_deplacer(plateau, 2):
            return -1
        else:
            return 0

def peut_deplacer(plateau, joueur):
    for ligne_index, ligne in enumerate(plateau):
        for case_index, case in enumerate(ligne):
            if case == joueur:
                if peut_sauter(plateau, joueur, ligne_index, case_index) or peut_deplacer_normal(plateau, joueur, ligne_index, case_index):
                    return True
    return False

def peut_sauter(plateau, joueur, ligne_index, case_index):
    if ligne_index >= 2 and case_index >= 2 and plateau[ligne_index-1][case_index-1] == joueur and plateau[ligne_index-2][case_index-2] == 0:
        return True
    if ligne_index >= 2 and case_index <= 1 and plateau[ligne_index-1][case_index+1] == joueur and plateau[ligne_index-2][case_index+2] == 0:
        return True
    if ligne_index <= 1 and case_index >= 2 and plateau[ligne_index+1][case_index-1] == joueur and plateau[ligne_index+2][case_index-2] == 0:
        return True
    if ligne_index <= 1 and case_index <= 1 and plateau[ligne_index+1][case_index+1] == joueur and plateau[ligne_index+2][case_index+2] == 0:
        return True
    return False

def peut_deplacer_normal(plateau, joueur, ligne_index, case_index):
    if ligne_index >= 1 and case_index >= 1 and plateau[ligne_index-1][case_index-1] == 0:
        return True
    if ligne_index >= 1 and case_index <= 2 and plateau[ligne_index-1][case_index+1] == 0:
        return True
    if ligne_index <= 2 and case_index >= 1 and plateau[ligne_index+1][case_index-1] == 0:
        return True
    if ligne_index <= 2 and case_index <= 2 and plateau[ligne_index+1][case_index+1] == 0:
        return True
    return False


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def afficher_regles():
    print("\033[1m\033[48;2;0;0;255mRègles du jeu de Dames:\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Le jeu se joue sur un plateau de 4x4 cases.\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Chaque joueur a 8 pions, représentés par des cercles pleins (●) ou vides (○).\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Les joueurs jouent à tour de rôle en déplaçant un de leurs pions.\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Si un pion atteint la dernière rangée de l'adversaire, il est promu en une dame et peut se déplacer dans toutes les directions.\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Le jeu se termine lorsque l'un des joueurs n'a plus que 1 pion ou qu'un joueur ne peut plus effectuer de déplacement.\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Le joueur qui capture tous les pions de l'adversaire ou qui empêche l'adversaire de faire un déplacement gagne la partie.\033[0m")

def main():   #bon
    clear_console()
    print("\033[1m\033[48;2;0;0;255mBienvenue dans le jeu des Canaries !\033[0m")
    print("Voulez vous afficher les règles du jeu ?")
    reponse = input("Entrez oui ou non : ")
    if reponse.lower() == "oui":
        afficher_regles()
    plateau = choisir_plateau()
    afficher_plateau(plateau)
    joueur = 1
    while True:
        deplacement = demander_mouvement(joueur)
        if deplacer_pion(plateau, deplacement[0], deplacement[1], joueur):
            clear_console()
            afficher_plateau(plateau)
            victoire = verifier_victoire(plateau)
            if victoire:
                print(f"\033[33m\033[1mLe joueur {victoire} a gagné !\033[0m")
                break
            joueur = 1 if joueur == 2 else 2
        else:
            print("\033[91mDeplacement invalide. Veuillez entrer un deplacement valide.\033[0m")

    print("Merci d'avoir joué !")


def test_choisir_plateau():
  pass


def test_afficher_plateau():
  pass


def test_demander_mouvement():
  pass


def test_valider_format_saisie():
  assert valider_format_saisie("A1 B2") == True, "Test 1: valider_format_saisie('A1 B2') == True"
  assert valider_format_saisie("A1B2") == False, "Test 2: valider_format_saisie('A1B2') == False"
  assert valider_format_saisie("A1 B 2") == False, "Test 3: valider_format_saisie('A1 B 2') == False"
  assert valider_format_saisie("A1 B2 ") == False, "Test 4: valider_format_saisie('A1 B2 ') == False"
  assert valider_format_saisie("A1XB2") == False, "Test 5: valider_format_saisie('A1XB2') == False"
  print("Tous les tests de valider_format_saisie() sont passés.")


def test_est_au_bon_format():
  assert est_au_bon_format("A1", "B2") == True, "Test 1: est_au_bon_format('A1', 'B2') == True"
  assert est_au_bon_format("A1", "B4") == True, "Test 2: est_au_bon_format('A1', 'B4') == True"
  assert est_au_bon_format("A1", "B5") == False, "Test 2: est_au_bon_format('A1', 'B5') == False"
  assert est_au_bon_format("A1", "E2") == False, "Test 3: est_au_bon_format('A1', 'E2') == False"
  assert est_au_bon_format("A1", "E5") == False, "Test 4: est_au_bon_format('A1', 'B') == False"
  assert est_au_bon_format("D5", "B2") == False, "Test 5: est_au_bon_format('D5', 'B2') == False"
  print("Tous les tests de est_au_bon_format() sont passés.")


def test_deplacer_pion():
  pass


def test_verifier_victoire():
  pass


def test_peut_deplacer():
  pass

def test_peut_sauter():
  assert peut_sauter(plateau_debut, 1, 0, 0) == True, "Test 1: peut_sauter(plateau_debut, 1, 0, 0) == True"
  print("Tous les tests de peut_sauter() sont passés.")

def test_peut_deplacer_normal():
  pass

test_choisir_plateau()
test_afficher_plateau()
test_demander_mouvement()
test_valider_format_saisie()
test_est_au_bon_format()
test_deplacer_pion()
test_verifier_victoire()
test_peut_deplacer()
test_peut_sauter()
test_peut_deplacer_normal()
print("Tout les tests sont passés.")

main()
