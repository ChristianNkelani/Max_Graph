#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:28:50 2024

@author: hitech
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CSVViewer:
    def __init__(self, root):
        self.root = root
        #self.root.attributes('-fullscreen', True)        
        self.root.title("HI-GRAPH")

        self.label = tk.Label(root, text="Sélectionnez un fichier CSV")
        self.label.pack(pady=10)

        self.button_browse = tk.Button(root, text="Parcourir", command=self.browse_file)
        self.button_browse.pack(pady=10)

        self.button_plot = tk.Button(root, text="Créer un graphique", command=self.create_plot, state=tk.DISABLED)
        self.button_plot.pack(pady=10)

        self.tree = ttk.Treeview(root)
        self.tree.pack(fill='both', expand=True)

        self.scroll_x = ttk.Scrollbar(root, orient="horizontal", command=self.tree.xview)
        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.scroll_y.pack(side="right", fill="y")

        self.tree.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        self.df = None

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.display_csv(self.df)
                self.button_plot.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire le fichier CSV:\n{e}")

    def display_csv(self, df):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        for index, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)

    def create_plot(self):
        if self.df is not None:
            self.show_bar_charts()

    def show_bar_charts(self):
        # Create a new window for the plot        
        # Données exemple
        categories = self.df.iloc[:, 0]
        print(categories)
        
        bar_width=0.15
        
        # Créer les positions des bâtonnets
        index = np.arange(len(categories))
        
        # Créer le graphique en bâtonnets
        fig, ax = plt.subplots()
        
   
       
        for i in range(1,self.df.shape[1]):
            # Bâtonnets pour la première série de données
            bar1 = ax.bar(index, self.df.iloc[:, i], bar_width)
            
            # Ajouter des titres et des étiquettes
            plt.xlabel('Minéraux')
            plt.ylabel('Concentration')
            plt.title('Graphique en bâtonnets')
            plt.xticks(rotation=45)
            index = index+ 0.15
        ax.set_xticklabels(categories)  # Définir les nouvelles étiquettes pour l'axe des x
        ax.legend()
        plt.tight_layout()
        
        # Afficher le graphique
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVViewer(root)
    root.mainloop()
