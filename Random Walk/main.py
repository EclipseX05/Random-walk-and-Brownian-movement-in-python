# main.py
import tkinter as tk
from tkinter import messagebox
import marche_1d
import marche_2d
import introduction
import mouvement_brownien

#demande à l'utilisateur quelle dimension chosiir
def start_simulation(choice):
    if choice == 1:
        introduction.run_intro()
    elif choice == 2:
        marche_1d.run_simulation_1d()
    elif choice == 3:
        marche_2d.run_simulation_2d()
    elif choice == 4:
        mouvement_brownien.run_simulation_mouvement_brownien()
    else:
        messagebox.showerror("Erreur", "Veuillez choisir une option valide.")

def main():
    root = tk.Tk()
    root.title("Simulation de Marche Aléatoire")

    label = tk.Label(root, text="Choisissez une option:")
    label.pack(pady=10)

    button_intro = tk.Button(root, text="Introduction", command=lambda: start_simulation(1))
    button_intro.pack()

    button_1d = tk.Button(root, text="Marche Aléatoire en 1D", command=lambda: start_simulation(2))
    button_1d.pack()

    button_2d = tk.Button(root, text="Marche Aléatoire en 2D", command=lambda: start_simulation(3))
    button_2d.pack()

    mouvement_brownien = tk.Button(root, text="Mouvement brownien", command=lambda: start_simulation(4))
    mouvement_brownien.pack()

    root.mainloop()

if __name__ == "__main__":
    main()

