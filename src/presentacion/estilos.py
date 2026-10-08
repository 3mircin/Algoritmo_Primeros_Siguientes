"""Paleta y estilos compartidos por los componentes de la interfaz (Modo Claro)."""

import tkinter as tk
from tkinter import ttk

COLORES = {
    "fondo": "#f3f4f6",          # Gris muy claro para el fondo principal
    "superficie": "#ffffff",     # Blanco puro para los paneles
    "superficie_alt": "#f9fafb", # Blanco roto para alternar en tablas
    "texto": "#111827",          # Casi negro para el texto principal
    "secundario": "#4b5563",     # Gris medio para subtítulos
    "primario": "#4f46e5",       # Índigo para botones y selecciones
    "primario_hover": "#4338ca", # Índigo oscuro al pasar el cursor
    "borde": "#d1d5db",          # Gris claro para los bordes
    "error": "#ef4444",          # Rojo
    "error_fondo": "#fee2e2",    # Rojo muy claro
    "exito": "#10b981",          # Verde esmeralda
}

def configurar_estilos(ventana):
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    
    # Estilos de botones
    estilo.configure(
        "TButton", font=("Segoe UI", 10), padding=(14, 8),
        background=COLORES["superficie"], foreground=COLORES["texto"],
        bordercolor=COLORES["borde"],
    )
    estilo.configure(
        "Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(16, 9),
        background=COLORES["primario"], foreground="white", borderwidth=0,
    )
    estilo.map("Accent.TButton", background=[("active", COLORES["primario_hover"])])
    
    # Estilos de tablas (Treeview)
    estilo.configure(
        "Treeview", background=COLORES["superficie_alt"], fieldbackground=COLORES["superficie_alt"],
        foreground=COLORES["texto"], rowheight=28, font=("Segoe UI", 10),
        bordercolor=COLORES["borde"],
    )
    estilo.configure(
        "Treeview.Heading", background="#e5e7eb", # Encabezados grises claros
        foreground=COLORES["texto"], font=("Segoe UI", 10, "bold"), padding=8,
    )
    # Al seleccionar una fila en modo claro, usamos el color primario con texto blanco
    estilo.map("Treeview", 
               background=[("selected", COLORES["primario"])],
               foreground=[("selected", "white")])
    
    # Estilos de pestañas (Notebook)
    estilo.configure("TNotebook", background=COLORES["fondo"], borderwidth=0)
    estilo.configure("TNotebook.Tab", padding=(18, 10), font=("Segoe UI", 10, "bold"), 
                     background=COLORES["borde"], foreground=COLORES["secundario"])
    estilo.map("TNotebook.Tab", 
               background=[("selected", COLORES["superficie"])],
               foreground=[("selected", COLORES["texto"])])

def crear_superficie(padre):
    return tk.Frame(
        padre, bg=COLORES["superficie"], highlightthickness=1,
        highlightbackground=COLORES["borde"],
    )