import numpy as np
import matplotlib.pyplot as plt

def run_simulation_mouvement_brownien():
    #nombre de pas
    num_steps = 1000

    #générer déplacement aléatoires
    dx = np.random.normal(0, 1, num_steps) #déplacements aléatoires en x
    dy = np.random.normal(0, 1, num_steps) #déplacements aléatoires en y

    #calcul des positions cumulatives
    x = np.cumsum(dx)
    y = np.cumsum(dy)

    #affichage graphique mouvement brownien
    plt.figure(figsize=(8, 6))
    plt.plot(x, y)
    plt.title('Mouvement Brownien en 2D')
    plt.xlabel('Position en x')
    plt.ylabel('Position en y')
    plt.grid(True)
    plt.show()