"""Controles tabulares reutilizables."""

import tkinter as tk
from tkinter import ttk

from .estilos import COLORES


def crear_tabla(padre, columnas, encabezados, anchos, alturas=28):
    marco = tk.Frame(padre, bg=COLORES["superficie"])
    tabla = ttk.Treeview(marco, columns=columnas, show="headings", selectmode="browse")
    for columna, encabezado, ancho in zip(columnas, encabezados, anchos):
        tabla.heading(columna, text=encabezado)
        tabla.column(columna, width=ancho, minwidth=60, anchor="w", stretch=True)
    tabla.configure(height=alturas)
    scroll_y = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
    scroll_x = ttk.Scrollbar(marco, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    tabla.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    marco.rowconfigure(0, weight=1)
    marco.columnconfigure(0, weight=1)
    return marco, tabla
