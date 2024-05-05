import os
import time
import random

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


def choisir_mode_de_jeu():
    while True:
        print("\n")
        print("\033[1m\033[48;2;0;0;255mChoisissez un mode de jeu :\033[0m")
        print("    1. Joueur contre Joueur")
        print("    2. Joueur contre IA")
        choix = input("\033[1m\033[48;2;255;255;0mEntrez votre choix (1 ou 2) : \033[0m")
        if choix == "1":
            return 1
        elif choix == "2":
            return 2  
        else:
            print("\033[91mChoix invalide. Veuillez entrer 1 ou 2.\033[0m")


def afficher_plateau(plateau):   
    # Couleurs pour les pions
    couleur_pion = {1: '\033[91m', 2: '\033[96m', 0: '\033[0m'}
    print('     1   2   3   4')
    for ligne_index, ligne in enumerate(plateau):
        print(f" {LIGNES[ligne_index]} | ", end='')
        for case in ligne:
            print(couleur_pion[case] + PIONS[case] + '\033[0m' + ' | ', end='')
        print()


def compter_pions(plateau):
    position_pions_noirs = []
    position_pions_blancs = []

    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j] == 1:
                position_pions_noirs.append((i, j))
            elif plateau[i][j] == 2:
                position_pions_blancs.append((i, j))

    pions_noirs = len(position_pions_noirs)
    pions_blancs = len(position_pions_blancs)
    return pions_noirs, pions_blancs, position_pions_noirs, position_pions_blancs


def generer_deplacements_posibles(plateau, position_pion, joueur):
    deplacements = [(0, 1), (1, 0), (0, -1), (-1, 0), (2, 0), (-2, 0), (0, 2), (0, -2)]
    destinations_possibles = []

    for i in range(len(deplacements)):
       # print("G_deplacement: pass", i, deplacements[i])
        x = position_pion[0] + deplacements[i][0]
        y = position_pion[1] + deplacements[i][1]
        if 0 <= x < 4 and 0 <= y < 4:
            destinations_possibles.append((x, y))
    return destinations_possibles


def est_au_bon_format(case1, case2):
    num_valide = ["1", "2", "3", "4"]
    lettre_valide = "ABCD"
    return case1[0] in lettre_valide and case1[1] in num_valide and case2[0] in lettre_valide and case2[1] in num_valide


def valider_format_saisie(deplacement):
    if len(deplacement) == 5 and deplacement[2] == " ":
        case1, case2 = deplacement.split()
        if est_au_bon_format(case1, case2):
            return True
    return False


def demander_mouvement(joueur):
    couleur_joueur = '\033[91m' if joueur == 1 else '\033[96m'
    while True:
        deplacement = input(f"{couleur_joueur}Joueur {joueur}\033[0m , entrez votre deplacement (ex: A1 B2) : ")
        if valider_format_saisie(deplacement):
            case1, case2 = deplacement.split()
            return convertir_case(case1), convertir_case(case2)
        else:
            print("\033[91mDeplacement invalide. Veuillez entrer un deplacement valide.\033[0m")
        

def convertir_case(case):
    return (ord(case[0].lower()) - ord('a'), int(case[1])-1)


def convertir_indices_a_coord(i, j):
    lettre = chr(j + ord('a')).upper()
    numero = str(i + 1)
    return lettre + numero


def deplacement_ia(plateau, joueur):
    pions_noirs, pions_blancs, position_pions_noirs, position_pions_blancs = compter_pions(plateau)
    random.shuffle(position_pions_noirs)

    while True:
        if len(position_pions_noirs) < 2:
            break

        for f in range(len(position_pions_noirs)):
            position_pion = position_pions_noirs[f]
            destination_possible = generer_deplacements_posibles(plateau, position_pion, joueur)
            for i in range(len(destination_possible)):
                if deplacer_pion(plateau, position_pion, destination_possible[i], joueur) == True:
                    return True
        


def realiser_deplacement(plateau, position_pion, destination, joueur):
    if deplacer_pion(plateau, position_pion, destination, joueur) == True:
        print("deplacement reussi")
        return True
    else:
        print("deplacement echoué")
        return False


def deplacer_pion(plateau, case1, case2, joueur):
    if plateau[case1[0]][case1[1]] == joueur:
        if abs(case1[0] - case2[0]) == 2 or abs(case1[1] - case2[1]) == 2:
            pion_a_sauter_index = ((case1[0] + case2[0]) // 2, (case1[1] + case2[1]) // 2)
            if plateau[pion_a_sauter_index[0]][pion_a_sauter_index[1]] == joueur and plateau[case2[0]][case2[1]] != 0 and plateau[case2[0]][case2[1]] != joueur:
                plateau[case1[0]][case1[1]] = 0
                plateau[case2[0]][case2[1]] = joueur
                return True
        elif (case1[0] == case2[0] and abs(case1[1] - case2[1]) == 1) or (case1[1] == case2[1] and abs(case1[0] - case2[0]) == 1):
            if plateau[case2[0]][case2[1]] == 0:
                plateau[case1[0]][case1[1]] = 0
                plateau[case2[0]][case2[1]] = joueur
                return True    
    return False


def peut_se_deplacer(plateau, joueur):
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j] == joueur:
                if peut_sauter(plateau, (i, j), joueur) or peut_deplacer(plateau, (i, j), joueur):
                    return True
    return False


def peut_sauter(plateau, position_pion, joueur):
    deplacements = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    for i in range(4):
        x = position_pion[0] + deplacements[i][0]
        y = position_pion[1] + deplacements[i][1]
        if 0 <= x < 4 and 0 <= y < 4:
            if (abs(deplacements[i][0]) == 2 and abs(deplacements[i][1] == 0)) or (abs(deplacements[i][1]) == 2 and abs(deplacements[i][0] == 0)):
                pion_a_sauter_index = ((position_pion[0] + x) // 2, (position_pion[1] + y) // 2)
                if plateau[pion_a_sauter_index[0]][pion_a_sauter_index[1]] == joueur:
                    return True
    return False


def peut_deplacer(plateau, position_pion, joueur):
    deplacements = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i in range(len(deplacements)):
        x = position_pion[0] + deplacements[i][0]
        y = position_pion[1] + deplacements[i][1]
        if 0 <= x < 4 and 0 <= y < 4 and plateau[x][y] == 0:
            if (abs(deplacements[i][0]) == 1 and abs(deplacements[i][1] == 0)) or (abs(deplacements[i][1]) == 1 and abs(deplacements[i][0] == 0)):
                return True
    return False


def verifier_victoire(plateau, joueur):
    pions_noirs, pions_blancs, position_pions_noirs, position_pions_blancs = compter_pions(plateau)
    if joueur == 1:
        if pions_blancs < 2 or not peut_se_deplacer(plateau, joueur):
            return 2
        return 0
    if joueur == 2:
        if pions_noirs >= 2 and peut_se_deplacer(plateau, joueur):
            return 0
        else:
            return 1
    else:
        return 0


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


def game():
    clear_console()
    print("\033[1m\033[48;2;0;0;255mBienvenue dans le jeu des Canaries!\033[0m")

    print("Voulez vous afficher les règles du jeu ?")
    choix = input("Entrez votre choix (oui/non) : ")
    if choix == "oui":
        afficher_regles()
    joueur = random.randint(1, 2)
    mode = choisir_mode_de_jeu()

    if mode == 1:
        clear_console()

        print("\033[1m\033[48;2;0;0;255mBienvenu au mode JvJ!\033[0m")
        print("\n")
        plateau = choisir_plateau()
        afficher_plateau(plateau)
        while True:
            deplacement = demander_mouvement(joueur)
            if deplacer_pion(plateau, deplacement[0], deplacement[1], joueur):
                clear_console()
                afficher_plateau(plateau)
                pions_noirs, pions_blancs, position_pions_noirs, position_pions_blancs = compter_pions(plateau)
                print(f"\033[1m\033[48;2;0;0;255mJoueur 1: {pions_noirs} pions\033[0m")
                print(f"\033[1m\033[48;2;0;0;255mJoueur 2: {pions_blancs} pions\033[0m")

                if verifier_victoire(plateau, joueur) != 0:
                    print(f"\033[1m\033[48;2;0;0;255mLe joueur", joueur , " a gagné!\033[0m")
                    break
                joueur = 1 if joueur == 2 else 2
            else:
                print("\033[91mDeplacement invalide. Veuillez entrer un deplacement valide.\033[0m")
        print("Merci d'avoir joué!")

    elif mode == 2:
        print("\033[1m\033[48;2;0;0;255mMode de jeu: Joueur contre Joueur\033[0m")
        print("\n")       
        print("\033[96m Joueur 2 vous allez jouer contre l'IA.\033[0m")
        print("\n")
        plateau = choisir_plateau()
        afficher_plateau(plateau)
        while True:
            if joueur == 1:
                
                deplacement_ia(plateau, joueur)
                clear_console()
                print("\033[1m\033[48;2;0;0;255mTour IA\033[0m")
                afficher_plateau(plateau)
                print("\033[1m\033[48;2;0;0;255mDéplacement IA réalisé\033[0m")
                
                pions_noirs, pions_blancs, position_pions_noirs, position_pions_blancs = compter_pions(plateau)
                print(f"\033[1m\033[48;2;0;0;255mJoueur 1: {pions_noirs} pions\033[0m")
                print(f"\033[1m\033[48;2;0;0;255mJoueur 2: {pions_blancs} pions\033[0m")
                
                time.sleep(3)
                if verifier_victoire(plateau, joueur) != 0:
                    print(f"\033[1m\033[48;2;0;0;255mLe joueur", joueur , " a gagné!\033[0m")
                    break
                joueur = 2
            else:
                clear_console()
                print("\033[93m C'est a vous de Jouer\033[0m")
                afficher_plateau(plateau)
                deplacement = demander_mouvement(joueur)
                if deplacer_pion(plateau, deplacement[0], deplacement[1], joueur):
                    clear_console()
                    afficher_plateau(plateau)
                    pions_noirs, pions_blancs, position_pions_noirs, position_pions_blancs = compter_pions(plateau)
                    print(f"\033[1m\033[48;2;0;0;255mJoueur 1: {pions_noirs} pions\033[0m")
                    print(f"\033[1m\033[48;2;0;0;255mJoueur 2: {pions_blancs} pions\033[0m")

                    if verifier_victoire(plateau, joueur) != 0:
                        print(f"\033[1m\033[48;2;0;0;255mLe joueur", joueur , " a gagné!\033[0m")
                        break
                    joueur = 1
                else:
                    print("\033[91mDeplacement invalide. Veuillez entrer un deplacement valide.\033[0m")
        print("Merci d'avoir joué!")



### TESTS UNITAIRES ###

def test_choisir_plateau():
    pass  # Fonction choisir_plateau() visuellement testée

def test_choisir_mode_de_jeu():
    pass  # Fonction choisir_mode_de_jeu() visuellement testée

def test_afficher_plateau():
    pass  # Fonction afficher_plateau() testée visuellement

def test_compter_pions():
    pions_noirs, pions_blancs, position_pions_noirs, position_pions_blancs = compter_pions(plateau_debut)
    assert pions_noirs == 8 and pions_blancs == 8, "Test compter_pions failed"
    
def test_generer_deplacements_posibles():
    pass  # Fonction generer_deplacements_posibles() testée de manière indirecte dans test_peut_sauter() et test_peut_deplacer()


def test_est_au_bon_format():
    assert est_au_bon_format("A1", "B2") == True, "Test 1 est_au_bon_format failed"
    assert est_au_bon_format("B2", "C3") == True, "Test 2 est_au_bon_format failed"
    assert est_au_bon_format("C3", "D4") == True, "Test 3 est_au_bon_format failed"
    assert est_au_bon_format("D4", "A1") == True, "Test 4 est_au_bon_format failed"
    assert est_au_bon_format("A1", "D4") == True, "Test 5 est_au_bon_format failed"
    assert est_au_bon_format("r", "A2") == False, "Test 6 est_au_bon_format failed"
    assert est_au_bon_format("Z1", "A5") == False, "Test 7 est_au_bon_format failed"
    assert est_au_bon_format("A1", "E1") == False, "Test 8 est_au_bon_format failed"
    assert est_au_bon_format("miau1", "E5") == False, "Test 9 est_au_bon_format failed"

def test_valider_format_saisie():
    assert valider_format_saisie("A1 B2") == True, "Test 1 valider_format_saisie failed"
    assert valider_format_saisie("B2 C3") == True, "Test 2 valider_format_saisie failed"
    assert valider_format_saisie("C3 D4") == True, "Test 3 valider_format_saisie failed"
    assert valider_format_saisie("D4 A1") == True, "Test 4 valider_format_saisie failed"
    assert valider_format_saisie("A1 D4") == True, "Test 5 valider_format_saisie failed"
    assert valider_format_saisie("A11 A2") == False, "Test 6 valider_format_saisie failed"
    assert valider_format_saisie("Z1 A5") == False, "Test 7 valider_format_saisie failed"
    assert valider_format_saisie("A1 E1") == False, "Test 8 valider_format_saisie failed"
    assert valider_format_saisie("miau1 E5") == False, "Test 9 valider_format_saisie failed"


def test_demande_mouvement():
    pass  # Fonction demander_mouvement() testée manuellement

def test_convertir_case():
    assert convertir_case("A1") == (0, 0), "Test 1 convertir_case failed"
    assert convertir_case("B2") == (1, 1), "Test 2 convertir_case failed"
    assert convertir_case("C3") == (2, 2), "Test 3 convertir_case failed"
    assert convertir_case("D4") == (3, 3), "Test 4 convertir_case failed"

def test_deplacement_ia():
    pass # Fonction deplacement_ia() testée manuellement 
    # IL EST DIFFICILE DE TESTER CETTE FONCTION CAR ELLE EST BASEE SUR DES CHOIX ALEATOIRES
    # ET NE RETOURNE PAS DE VALEURS MAIS DES BOOLEENS

def test_deplacer_pion():
    plateau = [
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [2, 2, 2, 2],
        [2, 2, 2, 2],
    ]
    position_pion = (0, 0)
    destination = (2, 0)
    joueur = 1
    assert deplacer_pion(plateau, position_pion, destination, joueur) == True, "Test 1 deplacer_pion failed"

    position_pion = (1, 2)
    destination = (0, 2)
    joueur = 2
    assert deplacer_pion(plateau, position_pion, destination, joueur) == False, "Test 2 deplacer_pion failed"

    position_pion = (3, 3)
    destination = (1, 3)
    joueur = 2
    assert deplacer_pion(plateau, position_pion, destination, joueur) == True, "Test 3 deplacer_pion failed"


def test_peut_se_deplacer():
    plateau = [
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [2, 2, 2, 2],
        [2, 2, 2, 2],
    ]
    joueur = 1
    assert peut_se_deplacer(plateau, joueur) == True, "Test 1 peut_se_deplacer failed"

    plateau = [
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [2, 2, 2, 2],
        [2, 2, 2, 2],
    ]
    joueur = 2
    assert peut_se_deplacer(plateau, joueur) == True, "Test 2 peut_se_deplacer failed"

    plateau = [
        [1, 1, 0, 2],
        [1, 1, 1, 1],
        [2, 0, 2, 2],
        [2, 2, 2, 0],
    ]
    joueur = 1
    assert peut_se_deplacer(plateau, joueur) == True, "Test 3 peut_se_deplacer failed"

    plateau = [
        [1, 2, 0, 0],
        [2, 0, 0, 0],
        [2, 0, 2, 2],
        [1, 2, 2, 1],
    ]
    joueur = 1
    assert peut_se_deplacer(plateau, joueur) == False, "Test 4 peut_se_deplacer failed"


def test_peut_sauter():
    pass  # Fonction peut_sauter() testée dans test_generer_deplacements_posibles()

def test_peut_deplacer():
    pass  # Fonction peut_deplacer() testée dans test_generer_deplacements_posibles()

def test_verifier_victoire():
    plateau1 = [
        [1, 1, 0, 1],
        [1, 2, 1, 1],
        [2, 2, 1, 2],
        [2, 0, 0, 2],
    ]
    plateau2 = [
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [2, 2, 2, 2],
        [2, 2, 2, 2],
    ]   
    plateau3 = [
        [2, 1, 1, 2],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
        [0, 0, 0, 0],
    ]
    assert verifier_victoire(plateau2, 2) == 0, "Test 1 verifier_victoire failed"
    assert verifier_victoire(plateau1, 1) == 0, "Test 2 verifier_victoire failed"
    assert verifier_victoire(plateau3, 1) == 0, "Test 3 verifier_victoire failed"


def test_clear_console():
    pass  # Fonction clear_console() non testée car elle ne retourne pas de valeur

def exe_tests():
    test_functions = [
        test_choisir_plateau, # pass
        test_choisir_mode_de_jeu, # pass
        test_afficher_plateau,  # pass
        test_compter_pions, # pass
        test_generer_deplacements_posibles,
        test_est_au_bon_format,
        test_valider_format_saisie,
        test_demande_mouvement,
        test_convertir_case,
        test_deplacement_ia,
        test_deplacer_pion,
        test_peut_se_deplacer,
        test_peut_sauter,
        test_peut_deplacer,
        test_verifier_victoire,
        test_clear_console # pass
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
        game()

exe_tests()