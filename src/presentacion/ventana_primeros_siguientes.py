"""Ventana que agrupa los resultados del algoritmo de Primeros y Siguientes."""

import sys
import tkinter as tk
from tkinter import ttk

from .estilos import COLORES, crear_superficie
from .tabla_conjuntos import TablaConjuntos

class VentanaPrimerosSiguientes(tk.Toplevel):
    def __init__(self, padre, primeros, siguientes):
        super().__init__(padre)
        self.title("Resultados: Primeros y Siguientes")
        self.geometry("900x600")
        self.minsize(700, 480)
        self.resizable(True, True)
        self.configure(bg=COLORES["fondo"])
        if sys.platform == "win32":
            self.wm_attributes("-toolwindow", False)

        # Cabecera
        cabecera = tk.Frame(self, bg=COLORES["fondo"])
        cabecera.pack(fill="x", padx=28, pady=(24, 14))
        tk.Label(
            cabecera, text="Cálculo de Primeros y Siguientes",
            font=("Segoe UI", 21, "bold"), bg=COLORES["fondo"],
            fg=COLORES["texto"],
        ).pack(anchor="w")
        tk.Label(
            cabecera, text="Conjuntos generados a partir de la gramática proporcionada.",
            font=("Segoe UI", 10), bg=COLORES["fondo"],
            fg=COLORES["secundario"],
        ).pack(anchor="w", pady=(4, 0))

        # Resumen superior
        resumen = crear_superficie(self)
        resumen.pack(fill="x", padx=28, pady=(0, 14))
        tk.Label(
            resumen, text=f"{len(primeros)} No Terminales analizados",
            font=("Segoe UI", 10, "bold"), bg=COLORES["superficie"],
            fg=COLORES["exito"],
        ).pack(side="left", padx=16, pady=12)

        # Cuerpo y pestañas
        cuerpo = crear_superficie(self)
        cuerpo.pack(fill="both", expand=True, padx=28, pady=(0, 24))
        pestañas = ttk.Notebook(cuerpo)
        pestañas.pack(fill="both", expand=True, padx=12, pady=12)

        # Creación de pestañas
        pestaña_primeros = tk.Frame(pestañas, bg=COLORES["superficie"])
        pestaña_siguientes = tk.Frame(pestañas, bg=COLORES["superficie"])
        pestañas.add(pestaña_primeros, text="  1. Primeros (First)  ")
        pestañas.add(pestaña_siguientes, text="  2. Siguientes (Follow)  ")

        # Inserción de las tablas en cada pestaña
        self.tabla_primeros = TablaConjuntos(pestaña_primeros, "Conjuntos de Primeros")
        self.tabla_primeros.pack(fill="both", expand=True, padx=8, pady=8)
        
        self.tabla_siguientes = TablaConjuntos(pestaña_siguientes, "Conjuntos de Siguientes")
        self.tabla_siguientes.pack(fill="both", expand=True, padx=8, pady=8)

        # Cargar los datos a las tablas
        self.tabla_primeros.mostrar(primeros)
        self.tabla_siguientes.mostrar(siguientes)