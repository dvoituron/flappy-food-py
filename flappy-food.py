import pygame
import random
import os

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de blocs")

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
bleu_opp = (132, 194, 166)
gris = (100, 100, 100)
rouge = (255, 0, 0)

# Chargement des images des brochettes
brochette_largeur = 400  # Largeur ajustée pour les brochettes
brochette_images = [
    pygame.transform.scale(pygame.image.load(os.path.join('images', f'brochette_{i}.png')), (brochette_largeur, hauteur)) # Charge, produit, Construit un nom de fichier et redimensionne
    for i in range(1, 4) # Nombre entre 1 et 3 qui est mit dans i
]
# Génération des versions inversées pour les blocs du haut
brochette_inversees = [pygame.transform.flip(img, False, True) for img in brochette_images]

# Paramètres des blocs gris
largeur_bloc = 40
hauteur_ouverture = 160
vitesse_bloc = 7
distance_paires = 300  # Distance constante entre les paires
nombre_paires = 5  # Nombre de paires visibles simultanément

# Génération initiale des blocs gris
def creer_blocs_gris():
    blocs = []
    for i in range(nombre_paires): # Genere nombres paires
        x = largeur + i * distance_paires # Meme distance entre chaque blocs
        ouverture_y = random.randint(hauteur_ouverture, hauteur - hauteur_ouverture) # Ouverture aleatoire entre 150 et 450
        bloc_haut = pygame.Rect(x, 0, largeur_bloc, ouverture_y - hauteur_ouverture // 2) # Blocs haut (0) jusque ouverture
        bloc_bas = pygame.Rect(x, ouverture_y + hauteur_ouverture //2, largeur_bloc, hauteur - ouverture_y - hauteur_ouverture // 2) # Blocs bas jusque ouverture
        # Chaque bloc a un type de brochette distinct
        brochette_haut_type = random.randint(0, 2) # 0, 1 ou 2
        brochette_bas_type = random.randint(0, 2) # 0, 1 ou 2
        blocs.append((bloc_haut, bloc_bas, brochette_haut_type, brochette_bas_type))
    return blocs

blocs_gris = creer_blocs_gris()



# Chargement des images du GIF (animation du hamburger)
image_gif = []
for i in range(1, 11):  # Assumer qu'il y a 10 images (de 1 à 10)
    gif_image = pygame.image.load(os.path.join('images', f'Hamburger-V2_{i}.gif'))
    gif_image = pygame.transform.scale(gif_image, (55, 55))  # Ajuster la taille de l'image
    image_gif.append(gif_image)

# Animation du GIF
current_frame = 0  # Index de l'image actuelle du GIF
frame_delay = 2  # Frame
frame_counter = 0  # Compteur pour contrôler le changement d'image du GIF

# Chargement de l'écran d'informations
ecran_informations = pygame.image.load(os.path.join('images', 'Fond informations.png'))
ecran_informations = pygame.transform.scale(ecran_informations, (largeur, hauteur))

# Chargement de l'écran d'accueil
ecran_attente = pygame.image.load(os.path.join('images', 'Fond ecran acceuil.png'))
ecran_attente = pygame.transform.scale(ecran_attente, (largeur, hauteur))

# Chargement de l'arrière-plan du jeu
arriere_plan = pygame.image.load(os.path.join('images', 'Fond python 1.png'))
arriere_plan = pygame.transform.scale(arriere_plan, (largeur*2, hauteur))

# Chargement musique de fond
pygame.mixer.music.load("sons/musique de fond.mp3")
# Chargement sound effect saut
son = pygame.mixer.Sound(os.path.join('sons', 'Saut.mp3'))
son.set_volume(0.5) # Volume entre 0.0 (silence) et 1.0 (maximum)




# Position initiale du fond
arriere_plan_x = 0
# Vitesse de défilement
scroll_speed = 3

# Police
font_path = os.path.join('Police', 'PressStart2P-Regular.ttf')
font = pygame.font.Font(font_path, 25)  # Taille de la police en pixels
title_text = font.render("Appuyez sur ESPACE pour jouer", True, (200, 200, 0))

# Affiche texte dans le jeu
def afficher_texte(text, x, y, couleur):
    texte = font.render(str(text), True, couleur) # Convertir chaine de caractere en surface graphique (True lisse les lettre)
    fenetre.blit(texte, (x, y)) # Blit affiche
# Stockage pour age et pseudo
def demander_pseudo_et_age():
    pseudo_valide = False
    age_valide = False
    pseudo = ""
    age = ""
    erreur_pseudo = ""
    erreur_age = ""
    actif = "pseudo"  # Pseudo puis age
    caractere = 0

    # Fin de la boucle quand pseudo et age ok
    while not (pseudo_valide and age_valide):
        for event in pygame.event.get(): #Examine chaque evenement de la fentre de jeu
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN: # Si une touche est enfoncee
                if event.key == pygame.K_RETURN:  # Touche entree pour valider
                    if actif == "pseudo":
                        # Validation du pseudo
                        if len(pseudo) < 3:
                            erreur_pseudo = f"{pseudo} doit etre de min 3 caractères."
                        elif not pseudo[0].isalpha():
                            erreur_pseudo = f"{pseudo} doit commencer par une lettre."
                        else:
                            pseudo_valide = True
                            actif = "age"  # Passer à l'âge
                            erreur_pseudo = "" # Enlever message de l'ecran
                    elif actif == "age":
                        # Validation de l'âge
                        try:
                            age = int(age)
                            if age > 0:
                                age_valide = True
                                erreur_age = ""
                            else:
                                erreur_age = "L'âge doit être positif."
                        except ValueError:
                            erreur_age = "Veuillez entrer un nombre valide."

                elif event.key == pygame.K_BACKSPACE:  # Retour arrière pour effacer
                    if actif == "pseudo":
                        caractere = 0
                        pygame.draw.rect(fenetre, (blanc), (300, 140, 20 - caractere, 40))
                        pseudo = pseudo[:-1]
                    elif actif == "age":
                        age = age[:-1]

                else:  # Ajouter caractères pour pseudo ou âge
                    if actif == "pseudo":
                        pseudo += event.unicode # Ajoute caractere pour pseudo
                    elif actif == "age":
                        age += event.unicode # Ajoute caractere pour age


        # Affichage de l'écran
        fenetre.blit(ecran_informations, (0, 0))  # Fond de demande d'informations

        # Dessiner le carré blanc sous informations
        pygame.draw.rect(fenetre, (blanc), (47, 40, 620, 40))        
        afficher_texte("Entrez vos informations :", 50, 50, noir)

        # Dessiner le carré blanc sous le pseudo
        pygame.draw.rect(fenetre, (blanc), (47, 140, 170, 40))
        # Affichage du pseudo
        afficher_texte("Pseudo: ", 50, 150, noir)
        afficher_texte(pseudo, 300, 150, noir) # La variable pseudo est l'element que l'utilisateur a ecrit
        if erreur_pseudo:
            afficher_texte(erreur_pseudo, 0, 200, rouge)

        # Dessiner le carré blanc sous l'âge
        pygame.draw.rect(fenetre, (blanc), (47, 290, 95, 40))  # Carré pour l'âge


        # Affichage de l'âge
        afficher_texte("Âge: ", 50, 300, noir)
        afficher_texte(age, 300, 300, noir) # La variable age est l'element que l'utilisateur a ecrit
        if erreur_age:
            afficher_texte(erreur_age, 0, 350, rouge)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    return pseudo, age

# Affiche pseudo et age dans la console
pseudo, age = demander_pseudo_et_age()
print(f"Pseudo: {pseudo}, Âge: {age}")

# Paramètres du personnage
imageX = 50  # Position fixe à gauche
imageY = (hauteur // 2) - 50 # Centrer verticalement au départ

# Paramètres de gravité et de saut
isJumping = False  # Pour vérifier si l'image est en train de sauter
jumpForce = -12  # Force du saut (remonter)
gravity = 1  # Force de gravité (descente)
velocityY = 0  # Vitesse verticale initiale

# Vitesse de déplacement de l'hamburger
moveSpeed = 20

score = 0

# Boucle de jeu
gameOn = False  # L'écran d'accueil doit apparaître au départ
running = True

while running:
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameOn:  # Si le jeu est déjà lancé et on appuie sur espace
                velocityY = jumpForce  # Appliquer la force de remontée
                isJumping = True
                son.play() # lancer le son
            if event.key == pygame.K_SPACE and not gameOn:  # Si l'écran d'accueil et l'utilisateur appuie sur espace
                gameOn = True
                pygame.mixer.music.play(-1)  # Démarre la musique de fond en boucle
        if event.type == pygame.QUIT:
            running = False


    if not gameOn:
        # Affichage de l'écran d'accueil
        fenetre.blit(ecran_attente, (0, 0))
        fenetre.blit(title_text, (largeur // 2 - title_text.get_width() // 2, hauteur // 2))
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        continue  # Empêche l'exécution de la logique du jeu

    fenetre.blit(arriere_plan, (0, 0))  # Afficher l'arrière-plan de jeu


    # Appliquer la gravité : le personnage descend
    if imageY + image_gif[current_frame].get_height() < hauteur:  # Si l'image n'a pas touché le bas
        velocityY += gravity
    else:
        velocityY = 0  # Arrêter la descente si l'on touche le bas

    # Mouvements verticaux
    imageY += velocityY  # Appliquer le mouvement vertical

    # Limite supérieure (haut de la fenêtre) : empêcher le personnage de sortir par le haut
    if imageY < 0:
        imageY = 0  # Empêcher de dépasser le haut de la fenêtre

    # Limite inférieure (bas de la fenêtre) : terminer le jeu si l'hamburger touche le sol
    if imageY + image_gif[current_frame].get_height() >= hauteur:
        print("Sol détecté !")
        running = False  # Fin du jeu

    # Mise à jour de la position du fond
    arriere_plan_x -= scroll_speed # Déplace le fond vers la gauche
    # Si le fond sort de l'écran, réinitialiser la position
    if arriere_plan_x <= -largeur*2:
        arriere_plan_x = 0
    # Mise à jour de l'affichage
    fenetre.fill((255, 255, 255)) # Optionnel : remplir d'une couleur pour éviter les artefacts
    fenetre.blit(arriere_plan, (arriere_plan_x, 0)) # Afficher l'image de fond
    # Afficher une seconde instance de l'image pour un défilement continu
    fenetre.blit(arriere_plan, (arriere_plan_x + largeur*2, 0)) # Afficher le fond décalé

    # Changement d'image du GIF
    frame_counter += 1
    if frame_counter >= frame_delay:  # Si le compteur atteint le délai (2 frames)
        current_frame += 1  # Passer à l'image suivante du GIF
        if current_frame >= len(image_gif):  # Si on a atteint la dernière image du GIF
            current_frame = 0  # Revenir à la première image pour boucler l'animation
        frame_counter = 0  # Réinitialiser le compteur pour le prochain délai

    # Affichage de l'image du GIF (l'hamburger reste à gauche)
    fenetre.blit(image_gif[current_frame], (imageX, imageY))




    # Défilement des blocs gris
    for i, (bloc_haut, bloc_bas, brochette_haut_type, brochette_bas_type) in enumerate(blocs_gris):
        bloc_haut.x -= vitesse_bloc
        bloc_bas.x -= vitesse_bloc 

        # Repositionner la paire de blocs lorsqu'elle sort de l'écran
        if bloc_haut.right < 0:
            dernier_bloc = max(bloc[0].x for bloc in blocs_gris)  # Trouver le dernier bloc visible
            bloc_haut.x = dernier_bloc + distance_paires
            bloc_bas.x = bloc_haut.x
            ouverture_y = random.randint(hauteur_ouverture, hauteur - hauteur_ouverture)
            bloc_haut.height = ouverture_y - hauteur_ouverture // 2
            bloc_bas.y = ouverture_y + hauteur_ouverture // 2
            bloc_bas.height = hauteur - bloc_bas.y
            # Assigner un nouveau type de brochette pour le haut et le bas
            blocs_gris[i] = (bloc_haut, bloc_bas, random.randint(0, 2), random.randint(0, 2))
            score += 1

    # Vérification des collisions
    for bloc_haut, bloc_bas, _, _ in blocs_gris:
        personnage_rect = pygame.Rect(imageX, imageY, image_gif[current_frame].get_width(), image_gif[current_frame].get_height())
        if personnage_rect.colliderect(bloc_haut) or personnage_rect.colliderect(bloc_bas):
            pygame.mixer.music.stop()  # Arrête la musique de fond
            running = False

    # Affichage des blocs gris avec les images des brochettes
    for bloc_haut, bloc_bas, brochette_haut_type, brochette_bas_type in blocs_gris:
        # Afficher les brochettes pour les blocs supérieurs
        fenetre.blit(brochette_inversees[brochette_haut_type],
                     (bloc_haut.x - (brochette_largeur - largeur_bloc) // 2,
                      bloc_haut.bottom - brochette_images[brochette_haut_type].get_height()))
        # Afficher les brochettes pour les blocs inférieurs
        fenetre.blit(brochette_images[brochette_bas_type],
                     (bloc_bas.x - (brochette_largeur - largeur_bloc) // 2,
                      bloc_bas.y))

    # Afficher le score
    font = pygame.font.Font(None, 36)
    texte_score = font.render(f"Score: {score}", True, (noir))
    fenetre.blit(texte_score, (10, 10))

    pygame.display.flip()  # Mettre à jour l'affichage

    # Contrôle de la vitesse de la boucle (FPS)
    pygame.time.Clock().tick(60)

# Quitter Pygame proprement
pygame.quit()
