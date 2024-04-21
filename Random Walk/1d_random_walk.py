import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

steps_range = []
moyenne_zero = []
predictions = []
graphique_analyse_fig = None  #variable pour stocker la figure du graphique d'analyse

def run_simulation_1d():
    def marche_aleatoire_1d(steps):
        position = 0
        positions = [position]
        for _ in range(steps):
            step = np.random.choice([-1, 1])  #déplacement aléatoire vers la gauche (-1) ou vers la droite (1)
            position += step
            positions.append(position)
        return positions

    def graphique_marche_aleatoire_simple():
        #nombre de pas pour la marche aléatoire, le nombre de pas est pas important, il faut juste qu'il soit assez grand pour montrer l'évolution
        plt.close('all')
        steps = 100

        #génération de la marche aléatoire en 1D
        positions = marche_aleatoire_1d(steps)

        #création du graphique
        global graphique_analyse_fig
        if graphique_analyse_fig is not None:
            plt.close(graphique_analyse_fig)  #fermer la figure précédente s'il existe encore

        graphique_analyse_fig = plt.figure(figsize=(10, 5))
        for i in range(steps):
            if positions[i + 1] > positions[i]:
                plt.arrow(i, positions[i], 0.5, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
            else:
                plt.arrow(i, positions[i], -0.5, 0, head_width=0.1, head_length=0.1, fc='red', ec='red')

        for i, position in enumerate(positions):
            if position == 0 and i > 0:
                plt.plot(i, position, marker='o', markersize=10, color='red', fillstyle='none', linestyle='None')

        plt.title("Marche aléatoire en 1D")
        plt.xlabel("Nombre de pas")
        plt.ylabel("Position")
        plt.grid(True)
        plt.show()

    def graphique_analyse():
        global steps_range
        global predictions
        global moyenne_zero
        global graphique_analyse_fig

        def retour_a_zero_moyen(steps, nb_simulations):
            moyenne_retours = []  # pour stocker les moyennes des fins sur zéro pour chaque pas
            for i in range(1, steps + 1):
                retour = 0
                for _ in range(1, nb_simulations + 1):
                    position = 0
                    for _ in range(1, i + 1):
                        step = random.randint(1, 2)  # déplacement aléatoire vers la gauche (-1) ou vers la droite (1)
                        if step == 1:
                            position -= 1
                        else:
                            position += 1
                    if position == 0:
                        retour += 1
                retour_final = retour / nb_simulations
                moyenne_retours.append(retour_final)
            new_moyenne_retours = moyenne_retours[1:-1:2]
            return new_moyenne_retours

        def prediction_statistique(steps):
            return 1 / np.sqrt(np.pi * steps)

        #récupérer les valeurs des entrées utilisateur
        steps = int(nb_steps_entry.get())
        if steps % 2 == 0:
            steps += 1
        nb_simulations = int(nb_simulations_entry.get())
        # préparation des données pour le graphique
        steps_range = range(1, steps, 2)
        moyenne_zero = retour_a_zero_moyen(steps, nb_simulations)
        predictions = [prediction_statistique(s) for s in steps_range]

        # création du graphique d'analyse
        global graphique_analyse_fig
        if graphique_analyse_fig is not None:
            plt.close(graphique_analyse_fig)  #fermer la figure précédente s'il existe encore

        graphique_analyse_fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        #graphique des simulations et des prédictions
        ax1.scatter(steps_range, moyenne_zero, label="Nombre de fins sur 0 moyenné")
        ax1.scatter(steps_range, predictions, label="Prédiction statistique")
        ax1.set_title("Nombre de fins sur 0 moyenné et prédiction statistique")
        ax1.set_xlabel("Nombre de pas")
        ax1.set_ylabel("Valeur")
        ax1.legend()
        ax1.grid(True)

        #graphique de l'écart entre les prédictions et les simulations
        ecarts = [abs(moyenne_zero[i] - predictions[i]) for i in range(len(moyenne_zero))]
        ax2.scatter(steps_range, ecarts, label="Écart entre simulations et prédictions")
        ax2.set_title("Écart entre simulations et prédictions")
        ax2.set_xlabel("Nombre de pas")
        ax2.set_ylabel("Écart")
        ax2.legend()
        ax2.grid(True)

        #ajustement de la mise en page pour éviter les chevauchements
        plt.tight_layout()
        plt.show()

    def afficher_ecart_moyen():
        def prediction_statistique(step):
            return 1/(np.sqrt(np.pi*step))

        def nombre_fins_sur_zero_moyen(steps, nb_simulations):
            prediction = []
            ecarts = []
            moyenne_retours = []
            nb_simulations = np.arange(1,nb_simulations+1,1)
            for i in nb_simulations: #création de données pour l'axe y 
                prediction_step = prediction_statistique(i)
                prediction.append(prediction_step)
                retour = 0
                for j in range (1,i+1) : #nombres de marches aléatoires à faire pour une moyenne
                    position = 0
                    for k in range(1, steps + 1): #simulation marche aléatoire
                        step = random.randint(1, 2) #déplacement aléatoire vers la gauche (-1) ou vers la droite (1)
                        if step == 1:
                            position -= 1
                        else:
                            position += 1
                    if position == 0:
                        retour += 1
                retour_final = retour / i
                moyenne_retours.append(retour_final)
                ecart = abs(abs(moyenne_retours[i-1])-abs(prediction[i-1]))
                ecarts.append(ecart)
            return nb_simulations,ecarts

        #création de la fenêtre Tkinter pour saisir les paramètres
        fenetre = tk.Toplevel()
        fenetre.title("Ecart moyen")
        fenetre.geometry("300x200")

        #saisie des paramètres par l'user
        label_pas = tk.Label(fenetre, text="Nombre de pas:")
        label_pas.pack()
        entry_pas = tk.Entry(fenetre)
        entry_pas.pack()

        label_simulations = tk.Label(fenetre, text="Nombre de simulations maximum:")
        label_simulations.pack()
        entry_simulations = tk.Entry(fenetre)
        entry_simulations.pack()

        #fonction pour calculer et afficher le graphique lorsque le bouton est cliqué
        def calculer_et_afficher():
            pas = int(entry_pas.get())
            simulations_max = int(entry_simulations.get())
            nb_simulations, ecarts = nombre_fins_sur_zero_moyen(pas, simulations_max)
    
            #création du graphique
            plt.figure(figsize=(8, 6))
            plt.plot(nb_simulations, ecarts, marker='o', linestyle='')
            plt.title("Nombre de fins sur 0 moyenné par rapport au nombre de simulations")
            plt.xlabel("Nombre de simulations")
            plt.ylabel("Nombre de fins sur 0 moyenné")
            plt.grid(True)
            plt.show()

        #bouton pour lancer le calcul
        bouton_calculer = tk.Button(fenetre, text="Calculer", command=calculer_et_afficher)
        bouton_calculer.pack()

    root = tk.Tk()
    root.title("Marche aléatoire en 1D")

    #cadre pour les paramètres de la marche aléatoire
    parameters_frame = tk.Frame(root)
    parameters_frame.pack(side=tk.LEFT, padx=10, pady=10)

    #nombre de pas (nb_steps)
    nb_steps_label = tk.Label(parameters_frame, text="Nombre de pas:")
    nb_steps_label.grid(row=0, column=0, padx=5, pady=5)
    nb_steps_entry = tk.Entry(parameters_frame)
    nb_steps_entry.grid(row=0, column=1, padx=5, pady=5)

    #nombre de simulations (nb_simulations)
    nb_simulations_label = tk.Label(parameters_frame, text="Nombre de simulations:")
    nb_simulations_label.grid(row=1, column=0, padx=5, pady=5)
    nb_simulations_entry = tk.Entry(parameters_frame)
    nb_simulations_entry.grid(row=1, column=1, padx=5, pady=5)

    #bouton pour afficher le graphique de la marche aléatoire simple
    graphique_simple_button = tk.Button(parameters_frame, text="Graphique d'une marche aléatoire en 1D", command=graphique_marche_aleatoire_simple)
    graphique_simple_button.grid(row=2, columnspan=2, padx=10, pady=10)

    #bouton pour afficher le graphique d'analyse
    afficher_button = tk.Button(parameters_frame, text="Afficher simulations", command=graphique_analyse)
    afficher_button.grid(row=3, columnspan=2, padx=10, pady=10)

    #bouton pour afficher l'écart moyen
    bouton_ecart_moyen = tk.Button(parameters_frame, text="Ecart moyen", command=afficher_ecart_moyen)
    bouton_ecart_moyen.grid(row=4, columnspan=2, padx=10, pady=10)

    #conteneur pour le graphique
    graphique_container = tk.Frame(root)
    graphique_container.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()


