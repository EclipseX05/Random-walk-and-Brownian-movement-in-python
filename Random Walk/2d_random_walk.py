import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

final_distances = None  #déclaration globale afin de l'utiliser plus tard

#encapsulation du code afin de permettre d'afficher quand user choisit 2d
def run_simulation_2d():

    #fonction qui calcule la distance finale moyenne pour une marche aléatoire en 2D
    def distance_finale(nb_steps, nb_simulations):
        global final_distances  # déclare globale afin de l'utiliser
        final_distances = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for steps in range(1, nb_steps + 1):
            distances = []
            for _ in range(nb_simulations):
                x, y = 0, 0
                for _ in range(steps):
                    index = np.random.randint(0, len(directions))
                    step = directions[index]
                    x += step[0]
                    y += step[1]
                distance = np.sqrt(x**2 + y**2)
                distances.append(distance)
            final_distances.append(np.mean(distances))
        return final_distances

    #fonction qui calcule l'écart entre la prédiction et la distance finale moyenne
    def calculer_ecart(nb_steps, final_distances):
        predictions = np.sqrt(np.arange(1, nb_steps + 1))
        ecart = np.abs(predictions - final_distances)
        return ecart

    #fonction appelée lorsque le bouton "Afficher" est cliqué pour le premier graphique
    def afficher_graphique():
        nb_steps = int(nb_steps_entry.get())
        nb_simulations = int(nb_simulations_entry.get())
        distance_finale(nb_steps, nb_simulations)
        predictions = np.sqrt(np.arange(1, nb_steps + 1))
        
        #supprimer le graphique précédent s'il existe
        for widget in graph_frame.winfo_children():
            widget.destroy()
        
        #création des figures Matplotlib avec deux sous-figures côte à côte
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        #premier graphique : Distance finale en fonction du nombre de pas
        ax1.scatter(range(1, nb_steps + 1), final_distances, marker='o', label='Distance finale moyenne')
        ax1.scatter(range(1, nb_steps + 1), predictions, label='Prédiction statistique (racine du nombre de pas)',linestyle = "--")
        ax1.set_title('Distance finale en fonction du nombre de pas')
        ax1.set_xlabel('Nombre de pas')
        ax1.set_ylabel('Distance finale moyenne')
        ax1.legend()
        ax1.grid(True)

        #deuxième graphique : Écart entre la prédiction et la distance finale moyenne
        ecart = calculer_ecart(nb_steps, final_distances)
        ax2.scatter(range(1, nb_steps + 1), ecart, marker='o', color='red')
        ax2.set_title('Écart entre la prédiction et la distance finale moyenne')
        ax2.set_xlabel('Nombre de pas')
        ax2.set_ylabel('Écart')
        ax2.grid(True)

        #affichage des sous-figures dans la fenêtre Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    #création de la fenêtre principale
    root = tk.Tk()
    root.title("Marche aléatoire en 2D")

    #cadre pour les paramètres de la marche aléatoire
    parameters_frame = tk.Frame(root)
    parameters_frame.pack(padx=10, pady=10)

    #nombre de pas
    nb_steps_label = tk.Label(parameters_frame, text="Nombre de pas:")
    nb_steps_label.grid(row=0, column=0, padx=5, pady=5)
    nb_steps_entry = tk.Entry(parameters_frame)
    nb_steps_entry.grid(row=0, column=1, padx=5, pady=5)

    #nombre de simulations
    nb_simulations_label = tk.Label(parameters_frame, text="Nombre de simulations:")
    nb_simulations_label.grid(row=1, column=0, padx=5, pady=5)
    nb_simulations_entry = tk.Entry(parameters_frame)
    nb_simulations_entry.grid(row=1, column=1, padx=5, pady=5)

    #bouton pour afficher le graphique
    afficher_button = tk.Button(root, text="Afficher simulations", command=afficher_graphique)
    afficher_button.pack(padx=10, pady=10)

    #cadre pour le graphique
    graph_frame = tk.Frame(root)
    graph_frame.pack(padx=10, pady=10)

    root.mainloop()
