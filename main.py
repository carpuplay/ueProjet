import os
import time

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
    [2, 1, 1, 2],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [0, 0, 0, 0],
]


LIGNES = {0: "A", 1: "B", 2: "C", 3: "D"}
PIONS = {0: " ", 1: "●", 2: "○"}

pions_noirs = 8
pions_blancs = 8


### FONCTIONS
def choisir_plateau():       
    plateau_dico = { '1': plateau_debut, '2': plateau_milieu, '3': plateau_fin }
    while True:
        print("\033[1m\033[48;2;0;0;255mChoisissez un plateau de jeu :\033[0m")
        choix = input("Entrez votre choix (1, 2 ou 3) : ")
        if choix in plateau_dico:
            return plateau_dico.get(choix)
        else:
            print("Choix invalide. Veuillez entrer 1, 2 ou 3.")


def afficher_plateau(plateau):   
    # Couleurs pour les pions
    couleur_pion = {1: '\033[91m', 2: '\033[96m', 0: '\033[0m'}
    print('     1   2   3   4')
    for ligne_index, ligne in enumerate(plateau):
        print(f" {LIGNES[ligne_index]} | ", end='')
        for case in ligne:
            print(couleur_pion[case] + PIONS[case] + '\033[0m' + ' | ', end='')
        print()


def demander_mouvement(joueur):   #Demande au joueur de rentrer un deplacement
    couleur_joueur = '\033[91m' if joueur == 1 else '\033[96m'
    while True:
        deplacement = input(f"{couleur_joueur}Joueur {joueur}\033[0m , entrez votre deplacement (ex: A1 B2) : ")
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

def est_au_bon_format(case1, case2):   #Verifie si les cases sont sous un format valide
  num_valide = ["1", "2", "3", "4"]
  lettre_valide = "ABCD"
  return case1[0] in lettre_valide and case1[1] in num_valide and case2[0] in lettre_valide and case2[1] in num_valide

def convertir_case(case):
    return (ord(case[0].lower()) - ord('a'), int(case[1])-1)


def deplacer_pion(plateau, case1, case2, joueur):   #Deplace un pion
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

def verifier_victoire(plateau, tour):
    pions_noirs, pions_blancs = compter_pions(plateau)
    
    if (pions_blancs < 2 and pions_noirs >= 2) or (not peut_deplacer(plateau, 2)):
        return 1  # Joueur 1 gagne
    elif (pions_noirs < 2 and pions_blancs < 2) or (not peut_deplacer(plateau, 1) and not peut_deplacer(plateau, 2)):
        return -1  # Egalité (peu probable mais evitie des bugs)
    elif (pions_noirs < 2 and pions_blancs >= 2) or (not peut_deplacer(plateau, 1)):
        return 2  # Le Joueur 2 gagne
    else:
        return 0  # Continúa el juego

def compter_pions(plateau):  #Compte les pions
    pions_noirs = 0
    pions_blancs = 0
    for ligne in plateau:
        for case in ligne:
            if case == 1:
                pions_noirs += 1
            elif case == 2:
                pions_blancs += 1
    return pions_noirs, pions_blancs



def peut_deplacer(plateau, joueur):     #Execute les fonctions de test de mouvement pour chaque case du jeux si il y a un pion
    for ligne_index, ligne in enumerate(plateau):
        for case_index, case in enumerate(ligne):
            if case == joueur:
                if peut_sauter(plateau, joueur, ligne_index, case_index) or peut_deplacer_normal(plateau, joueur, ligne_index, case_index):
                    return True
    return False

def peut_sauter(plateau, joueur, ligne_index, case_index): #Fonction qui verifie si un pion peut realiser un deplacement en saut
    if ligne_index >= 2 and case_index >= 2 and plateau[ligne_index-1][case_index-1] != 0 and plateau[ligne_index-1][case_index-1] != joueur and plateau[ligne_index-2][case_index-2] == 0:
        return True
    elif ligne_index >= 2 and case_index <= len(plateau[0]) - 3 and plateau[ligne_index-1][case_index+1] != 0 and plateau[ligne_index-1][case_index+1] != joueur and plateau[ligne_index-2][case_index+2] == 0:
        return True
    elif ligne_index <= len(plateau) - 3 and case_index >= 2 and plateau[ligne_index+1][case_index-1] != 0 and plateau[ligne_index+1][case_index-1] != joueur and plateau[ligne_index+2][case_index-2] == 0:
        return True
    elif ligne_index <= len(plateau) - 3 and case_index <= len(plateau[0]) - 3 and plateau[ligne_index+1][case_index+1] != 0 and plateau[ligne_index+1][case_index+1] != joueur and plateau[ligne_index+2][case_index+2] == 0:
        return True
    return False


def peut_deplacer_normal(plateau, joueur, ligne_index, case_index): #Fontion qui verifie si un pion peut realiser un deplacement simple
    if ligne_index >= 1 and case_index >= 1 and plateau[ligne_index-1][case_index-1] == 0:
        return True
    if ligne_index >= 1 and case_index <= len(plateau[0]) - 2 and plateau[ligne_index-1][case_index+1] == 0:
        return True
    if ligne_index <= len(plateau) - 2 and case_index >= 1 and plateau[ligne_index+1][case_index-1] == 0:
        return True
    if ligne_index <= len(plateau) - 2 and case_index <= len(plateau[0]) - 2 and plateau[ligne_index+1][case_index+1] == 0:
        return True
    return False


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def afficher_regles():
    print("\033[1m\033[48;2;0;0;255mRègles du jeu des Canaries:\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Le jeu se joue sur un plateau de 4x4 cases.\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Chaque joueur a 8 pions au début de la partie.\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Il existe deux types de déplacements : le déplacement simple et le déplacement de capture.\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Le déplacement simple se réalise orthogonalement (comme la tour aux échecs) et est de distance 1.\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Le déplacement de capture est possible si et seulement si le pion à capturer est à distance 2, et qu'il existe un pion du même camp que celui de départ entre les deux.\033[0m")
    print("\033[1m\033[48;2;0;0;255m- Le jeu se termine lorsque l'un des joueurs a moins de 2 pions ou en cas d'échec mat (impossibilité de continuer à se déplacer).\033[0m")


def main():   
    clear_console()
    print("""       _.--.__                                             _.--.
              ./'       `--.__                                   ..-'   ,' 
            ,/               |`-.__                            .'     ./
           :,                 :    `--_    __                .'   ,./'_.....-'
            :                  :   /    `-:' _\.            .'   ./..-'   _.'
            :                  ' ,'       : / \ :         .'    `-'__...-'
            `.               .'  .        : \@/ :       .'       '------.,
              ._....____  ./    :     .. `     :    .-'      _____.----'
                        `------------' : |     `..-'        `---.
                                   .---'  :    ./      _._-----'
          .---------._____________ `-.__/ : /`      ./_-----/':
          `---...--.              `-_|    `.`-._______-'  /  / ,-----.__----.
             ,----' ,__.  .          |   /  `\.________./  ====__....._____.'
             `-___--.-' ./. .-._-'----\.                  ./.---..____.--.
                   :_.-' '-'            `..            .-'===.__________.'
                                           `--...__.--'
          \033[1m\033[48;2;0;0;255mBienvenue dans le jeu des Canaries !\033[0m
          """)

    print("Voulez vous afficher les règles du jeu ?")
    reponse = input("Entrez oui ou non : ")
    if reponse.lower() == "oui":
        afficher_regles()
    plateau = choisir_plateau()
    afficher_plateau(plateau)
    joueur = 1
    while True:  # Boucle de jeu
        deplacement = demander_mouvement(joueur)
        if deplacer_pion(plateau, deplacement[0], deplacement[1], joueur):
            clear_console()
            afficher_plateau(plateau)
            pions_noirs, pions_blancs = compter_pions(plateau)  # Compter les pions
            print(f"Joueur 1: {pions_noirs} pions")
            print(f"Joueur 2: {pions_blancs} pions")
            victoire = verifier_victoire(plateau, joueur)  # Vérifier si un joueur a gagné
            if victoire:
                print(f"\033[33m\033[1mLe joueur {victoire} a gagné !\033[0m")
                break
            joueur = 1 if joueur == 2 else 2
        else:   # Si le déplacement est invalide
            print("\033[91mDeplacement invalide. Veuillez entrer un deplacement valide.\033[0m")

    print("Merci d'avoir joué !")



def test_choisir_plateau():
    pass                                               #inutile de tester cette fonction car elle utilise input()


def test_afficher_plateau():
    pass                                               #inutile de tester cette fonction car elle utilise print()


def test_demander_mouvement():
    pass                                                #inutile de tester cette fonction car elle utilise input()


def test_valider_format_saisie():
    assert valider_format_saisie("A1 B2") == True
    assert valider_format_saisie("A1B2") == False
    assert valider_format_saisie("A1 B 2") == False
    assert valider_format_saisie("A1 B2 ") == False
    assert valider_format_saisie("A1XB2") == False



def test_est_au_bon_format():
    assert est_au_bon_format("A1", "B2") == True
    assert est_au_bon_format("A1", "B4") == True
    assert est_au_bon_format("A1", "B5") == False
    assert est_au_bon_format("A1", "E2") == False
    assert est_au_bon_format("A1", "E5") == False
    assert est_au_bon_format("D5", "B2") == False
    #  Cette fonction verifie aussi si les cases sont bien dans le plateau!!! 


def test_deplacer_pion():
    plateau = [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [2, 2, 2, 2],
        [2, 2, 2, 2],
    ]
    assert deplacer_pion(plateau, "A1", "C1", 1) == True
    assert deplacer_pion(plateau, "A1", "A2", 1) == False


def test_verifier_victoire():
    plateau1 = [
        [0, 0, 0, 0],
        [0, 0, 2, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
    assert verifier_victoire(plateau1, 1) == 1, "Test 1" 
    
    plateau = [
        [2, 2, 0, 0],
        [2, 2, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    assert verifier_victoire(plateau, 1) == 2, "Test 2"
    


def test_peut_deplacer():
    plateau = [
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [2, 2, 2, 2],
        [2, 2, 2, 2],
    ]
    assert peut_deplacer(plateau,1) == True, "Test 1"

def test_peut_sauter():
    pass                                     #inutile de tester cette fonction car elle est utilisée dans peut_deplacer()


def test_peut_deplacer_normal():
    plateau2 = [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [2, 2, 2, 2],
        [2, 2, 2, 2],
    ]
    assert peut_deplacer_normal(plateau2, 1, 0, 0) == False, "Test 1: peut_deplacer_normal(plateau, 1, 0, 0) == False"
    assert peut_deplacer_normal(plateau2, 2, 0, 0) == False, "Test 2: peut_deplacer_normal(plateau, 2, 0, 0) == False"
    
    plateau = [
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [2, 2, 2, 2],
        [2, 2, 2, 2],
    ]
    assert peut_deplacer_normal(plateau, 1, 0, 0) == False, "Test 3: peut_deplacer_normal(plateau, 1, 0, 0) == False"
    assert peut_deplacer_normal(plateau, 2, 0, 0) == False, "Test 4: peut_deplacer_normal(plateau, 2, 0, 0) == False"
    
    plateau = [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [2, 0, 0, 0],
        [0, 2, 0, 0],
    ]
    assert peut_deplacer_normal(plateau, 1, 0, 0) == False, "Test 5: peut_deplacer_normal(plateau, 1, 0, 0) == True"
    assert peut_deplacer_normal(plateau, 2, 0, 0) == False, "Test 6: peut_deplacer_normal(plateau, 2, 0, 0) == True"
    
    plateau = [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [2, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    assert peut_deplacer_normal(plateau, 1, 0, 0) == False, "Test 7: peut_deplacer_normal(plateau, 1, 0, 0) == False"
    assert peut_deplacer_normal(plateau, 2, 0, 0) == False, "Test 8: peut_deplacer_normal(plateau, 2, 0, 0) == False"
    


def exe_tests():
    test_functions = [
        test_choisir_plateau,
        test_afficher_plateau,
        test_demander_mouvement,
        test_valider_format_saisie,
        test_est_au_bon_format,
        test_deplacer_pion,
        test_verifier_victoire, 
        test_peut_deplacer,
        test_peut_sauter,
        test_peut_deplacer_normal
    ]
    total_tests = len(test_functions)
    tests_passed = 0
    tests_failed = 0
    clear_console()
    print("Vérification des fonctions...")
    for i, test_func in enumerate(test_functions, start=1):
        time.sleep(0.5)  # Simule le temps d'exécution d'un test
        print(f"Éxecution du test {i}/{total_tests}...")
        try:
            test_func()  # Appel de la fonction de test
            tests_passed += 1
            print(f"\033[32mTest {i}/{total_tests} réussi\033[0m")  # Couleur verte pour les tests réussis
        except AssertionError as e:
            tests_failed += 1
            print(f"\033[31mTest {i}/{total_tests} échoué: {e}\033[0m")  # Couleur rouge pour les Assertions échoués
        except Exception as e:
            tests_failed += 1
            print(f"\033[31mTest {i}/{total_tests} échoué: {e}\033[0m")  # Couleur rouge pour les Exceptions échoués

    print("\nRésultats des Tests:")
    print(f"Tests réussits: \033[32m{tests_passed}/{total_tests}\033[0m")  # Couleur verte pour les tests réussis
    print(f"Tests échoués: \033[31m{tests_failed}/{total_tests}\033[0m")  # Couleur rouge pour les tests échoués
    print("\033[1m\033[48;2;0;0;255m\nVoulez vous lancer le jeux?\033[0m")

    reponse = input("Entrez oui ou non : ")
    if reponse.lower() == "oui":     #rend l'affichage plus dynamique 
        for i in range(3):
            clear_console()
            print("\033[5;37;40mExecution du programme principal...\033[0m") 
            time.sleep(0.5)
            clear_console()
            print("\033[5;30;40mExecution du programme principal...\033[0m") 
            time.sleep(0.5)
            i += 1
        main()
    


exe_tests()
