import numpy as np
import matplotlib.pyplot as plt
import random

# Paramètres de simulation
grid_size = 600  # Taille de la grille
num_particles = 5000  # Nombre total de particules à simuler
stick_radius = 1  # Distance à laquelle une particule peut "coller" à la structure
start_point = (grid_size // 2, 0)  # Point de départ de la graine (le nuage)
max_steps = 3000  # Nombre maximal de pas pour une particule

# Création de la grille avec une graine initiale (la graine de foudre)
grid = np.zeros((grid_size, grid_size), dtype=bool)
grid[start_point] = True  # La graine initiale est au sommet de la grille

# Fonction pour générer une nouvelle particule à un endroit aléatoire sur le bord supérieur
def generate_new_particle(grid_size):
    return (random.randint(0, grid_size-1), grid_size-1)  # Nouvelle particule sur le bord supérieur

# Fonction pour vérifier si une particule touche la structure existante
def is_touching_structure(x, y, grid):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            # Vérifie que (x + dx) et (y + dy) restent dans les limites de la grille
            if 0 <= x + dx < grid.shape[0] and 0 <= y + dy < grid.shape[1]:
                if grid[x + dx, y + dy]:
                    return True
    return False

# Fonction de marche aléatoire pour la particule
def random_walk(x, y, grid_size):
    direction = random.choices([(1, 0), (-1, 0), (0, 1), (0, -1)], weights=[1, 1, 1, 6])[0]  # Plus de chance de descendre
    x_new, y_new = x + direction[0], y + direction[1]
    
    # S'assurer que la particule reste dans la grille
    x_new = max(0, min(x_new, grid_size - 1))
    y_new = max(0, min(y_new, grid_size - 1))
    
    return x_new, y_new

# Simulation de DLA (Diffusion-Limited Aggregation)
for i in range(num_particles):
    # Générer une nouvelle particule
    x, y = generate_new_particle(grid_size)
    
    # Réinitialiser le nombre de pas pour chaque particule
    step = 0
    
    # Faire marcher la particule jusqu'à ce qu'elle touche la structure ou atteigne le nombre maximal de pas
    while step < max_steps:
        x, y = random_walk(x, y, grid_size)
        
        # Si la particule touche la structure, elle s'attache
        if is_touching_structure(x, y, grid):
            grid[x, y] = True
            print(f"Particule {i+1} attachée après {step} pas")
            break  # Sortir de la boucle dès que la particule s'attache
        
        step += 1
    

# Visualisation de la trajectoire de la foudre
# Code existant
plt.imshow(grid.T, cmap='binary', origin='lower')
plt.title("Simulation de la foudre (DLA)")

# Enregistre l'image
plt.savefig('simulation_foudre.png')

# Affiche l'image
plt.show()