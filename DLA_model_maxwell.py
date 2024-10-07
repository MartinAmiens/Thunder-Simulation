import numpy as np
import matplotlib.pyplot as plt
import random

# Paramètres de simulation
grid_size = 25
num_particles = 20
stick_radius = 1
start_point = (grid_size // 2, grid_size)
max_steps = 600000
E_field = np.random.uniform(low=0, high=2e6, size=(grid_size, grid_size, 2))
charge_part = 1
ionization_threshold = 1e6
ionization_probability = 0.1
grid = np.zeros((grid_size, grid_size), dtype=bool)
grid[start_point] = True

def generate_new_particle(grid_size):
    return (grid_size//2, grid_size-1)

def is_touching_structure(x, y, grid, stick_radius=1):
    for dx in range(-stick_radius, stick_radius+1):
        for dy in range(-stick_radius, stick_radius+1):
            if 0 <= x + dx < grid.shape[0] and 0 <= y + dy < grid.shape[1]:
                if grid[x + dx, y + dy]:
                    return True
    return False

def ionization_movement(x, y, grid_size, E_field, charge, ionization_threshold, ionization_probability):
    Ex, Ey = E_field[x][y]
    if abs(Ex) + abs(Ey) > ionization_threshold:
        if random.random() < ionization_probability:
            direction_x = charge * Ex * 0.01
            direction_y = charge * Ey * 0.01
        else:
            direction_x, direction_y = random.choices([(1, 0), (-1, 0), (0, 1), (0, -1)], weights=[1, 1, 1, 1])[0]
    else:
        direction_x, direction_y = random.choices([(1, 0), (-1, 0), (0, 1), (0, -1)], weights=[1, 1, 1, 1])[0]
    
    x_new = max(0, min(x + int(direction_x), grid_size - 1))
    y_new = max(0, min(y + int(direction_y), grid_size - 1))
    
    return x_new, y_new

# Simulation de DLA
trajectories = []
for i in range(num_particles):
    x, y = generate_new_particle(grid_size)
    trajectory = [(x, y)]
    step = 0
    while step < max_steps:
        x, y = ionization_movement(x, y, grid_size, E_field, charge_part, ionization_threshold, ionization_probability)
        trajectory.append((x, y))
        if is_touching_structure(x, y, grid, stick_radius):
            grid[x, y] = True
            print(f"Particule {i+1} attachée après {step} pas")
            break
        step += 1
    trajectories.append(trajectory)

# Visualisation
for trajectory in trajectories:
   xs, ys = zip(*trajectory)
   plt.plot(xs, ys, alpha=0.5)
plt.imshow(grid.T, cmap='binary', origin='lower')
plt.title("Simulation de la foudre (DLA) avec trajectoires")
plt.savefig('simulation_foudre_plus_trajectories.png')
plt.show()
