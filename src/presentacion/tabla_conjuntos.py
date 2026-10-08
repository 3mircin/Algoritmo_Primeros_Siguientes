
import tkinter as tk
from .estilos import COLORES
from .tabla_base import crear_tabla

class TablaConjuntos(tk.Frame):
    def __init__(self, padre, titulo_tabla):
        super().__init__(padre, bg=COLORES["superficie"])
        self.funcion = "PRIMERO" if "Primeros" in titulo_tabla else "SIGUIENTE"
        tk.Label(
            self, text=titulo_tabla,
            font=("Segoe UI", 11, "bold"), bg=COLORES["superficie"],
            fg=COLORES["texto"],
        ).pack(fill="x", padx=8, pady=(4, 10))
        
        # Dos columnas: No Terminal y su Conjunto
        self.marco, self.tabla = crear_tabla(
            self, ("no_terminal", "conjunto"),
            ("Símbolo", "Salida"), (150, 500), 16,
        )
        self.marco.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def mostrar(self, diccionario_conjuntos):
        """
        Recibe un diccionario donde la clave es el No Terminal 
        y el valor es un set() o list() con los terminales.
        """
        self.tabla.delete(*self.tabla.get_children())
        for no_terminal, conjunto in diccionario_conjuntos.items():
            elementos = " ".join(sorted(conjunto))
            representacion = f"{self.funcion}({no_terminal}) = {{ {elementos} }}"
            
            self.tabla.insert(
                "", tk.END,
                values=(no_terminal, representacion),
            )