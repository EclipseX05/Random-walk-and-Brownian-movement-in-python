import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def run_intro():
    #fonction pour la marche aléatoire en 1D
    def marche_aleatoire_1d(steps):
        x = 0
        positions_x = [x]
        directions = [-1, 1]  #déplacements possibles (gauche, droite)
        for _ in range(steps):
            dx = np.random.choice(directions)  #sélectionner aléatoirement une direction
            x += dx
            positions_x.append(x)
        return positions_x

    #fonction pour la marche aléatoire en 2D
    def marche_aleatoire_2d(steps):
        x, y = 0, 0
        positions_x = [x]
        positions_y = [y]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  #déplacements possibles (droite, gauche, haut, bas)
        for _ in range(steps):
            dx, dy = directions[np.random.randint(0, 4)]  #sélectionner aléatoirement une direction
            x += dx
            y += dy
            positions_x.append(x)
            positions_y.append(y)
        return positions_x, positions_y

    #fonction pour afficher l'interface Tkinter et gérer les simulations
    def run_simulation():
        #création de la fenêtre principale
        root = tk.Tk()
        root.title("Simulation de marche aléatoire")

        #cadre pour les paramètres
        parameters_frame = tk.Frame(root)
        parameters_frame.pack(padx=10, pady=10)

        #label pour le choix de dimension
        dimension_label = tk.Label(parameters_frame, text="Choisissez la dimension de la marche aléatoire:")
        dimension_label.grid(row=0, column=0, padx=5, pady=5)

        #menu déroulant pour choisir la dimension
        dimension_var = tk.StringVar(root)
        dimension_var.set("1D")  # Initialisation à 1D
        dimension_menu = tk.OptionMenu(parameters_frame, dimension_var, "1D", "2D")
        dimension_menu.grid(row=0, column=1, padx=5, pady=5)

        #label pour le nombre de pas
        steps_label = tk.Label(parameters_frame, text="Nombre de pas:")
        steps_label.grid(row=1, column=0, padx=5, pady=5)

        #entrée pour saisir le nombre de pas
        steps_entry = tk.Entry(parameters_frame)
        steps_entry.grid(row=1, column=1, padx=5, pady=5)

        #zone de texte pour afficher les coordonnées et l'écart final en 2D
        text_output = tk.Text(root, height=15, width=50)
        text_output.pack(padx=10, pady=10)

        #création d'une figure et d'un canevas pour les graphiques
        fig, ax = plt.subplots()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        #fonction pour démarrer la simulation
        def start_simulation():
            dimension = dimension_var.get()
            steps = int(steps_entry.get())

            text_output.delete(1.0, tk.END)  #effacer le contenu précédent

            if dimension == "1D":
                positions_x = marche_aleatoire_1d(steps)
                ax.clear()  #effacer le graphique précédent
                ax.plot(positions_x, [0]*len(positions_x), marker='o', markersize=4, linestyle='--', color='blue')
                ax.set_title("Marche aléatoire en 1D")
                ax.set_xlabel("Position en x")
                ax.set_ylabel("Position en y")
                ax.grid(True)
                canvas.draw()
                for i, pos in enumerate(positions_x):
                    text_output.insert(tk.END, f"Étape {i+1}: x = {pos}\n")
                if positions_x[-1] == 0:
                    text_output.insert(tk.END, f"\nLa marche aléatoire a finit sur la position 0.")
            elif dimension == "2D":
                positions_x, positions_y = marche_aleatoire_2d(steps)
                ax.clear()  #effacer le graphique précédent
                ax.plot(positions_x, positions_y, marker='o', markersize=4, linestyle='--', color='blue')
                ax.set_title("Marche aléatoire en 2D")
                ax.set_xlabel("Position en x")
                ax.set_ylabel("Position en y")
                ax.grid(True)
                canvas.draw()
                for i, (x, y) in enumerate(zip(positions_x, positions_y)):
                    text_output.insert(tk.END, f"Étape {i+1}: x = {x}, y = {y}\n")
                final_distance = abs(positions_x[-1]) + abs(positions_y[-1])
                text_output.insert(tk.END, f"\nEcart final après la 100ème étape : {final_distance:.2f}\n")

        #bouton pour démarrer la simulation
        start_button = tk.Button(root, text="Démarrer la simulation", command=start_simulation)
        start_button.pack(padx=10, pady=10)

        root.mainloop()

    #lancer la simulation
    run_simulation()
