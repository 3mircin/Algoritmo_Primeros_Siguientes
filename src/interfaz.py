"""Punto de entrada de la interfaz gráfica de Primeros y Siguientes."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from persistencia.algoritmo_primeros import calcular_primeros
from persistencia.algoritmo_siguientes import calcular_siguientes
from persistencia.lector_archivo import cargar_gramatica_desde_archivo
from presentacion.estilos import COLORES, configurar_estilos, crear_superficie
from presentacion.ventana_primeros_siguientes import VentanaPrimerosSiguientes


class InterfazCompilador(tk.Tk):
    """Ventana principal para cargar una gramática y calcular sus conjuntos."""

    def __init__(self):
        super().__init__()
        self.ruta_actual = ""
        self.gramatica = None
        self.ventana_resultados = None

        self.title("Primeros y Siguientes · Analizador de gramáticas")
        self.geometry("1180x760")
        self.minsize(900, 600)
        self.resizable(True, True)
        self.configure(bg=COLORES["fondo"])
        configurar_estilos(self)
        self._crear_interfaz()

    def _crear_interfaz(self):
        cabecera = tk.Frame(self, bg=COLORES["fondo"])
        cabecera.pack(fill="x", padx=34, pady=(26, 14))
        tk.Label(
            cabecera, text="Analizador de gramáticas",
            font=("Segoe UI", 24, "bold"), bg=COLORES["fondo"],
            fg=COLORES["texto"],
        ).pack(anchor="w")
        tk.Label(
            cabecera,
            text="Carga una gramática y consulta sus conjuntos de Primeros y Siguientes.",
            font=("Segoe UI", 11), bg=COLORES["fondo"],
            fg=COLORES["secundario"],
        ).pack(anchor="w", pady=(4, 0))

        controles = crear_superficie(self)
        controles.pack(fill="x", padx=34, pady=(0, 18))
        self.ruta_var = tk.StringVar(value="Ningún archivo seleccionado")
        tk.Label(
            controles, textvariable=self.ruta_var, anchor="w",
            font=("Segoe UI", 10), bg=COLORES["superficie"],
            fg=COLORES["secundario"],
        ).pack(side="left", fill="x", expand=True, padx=16, pady=12)
        ttk.Button(
            controles, text="Analizar", style="Accent.TButton",
            command=self.analizar,
        ).pack(side="right", padx=(4, 8), pady=8)
        ttk.Button(
            controles, text="Cargar archivo", command=self.abrir_archivo,
        ).pack(side="right", padx=8, pady=8)
        ttk.Button(
            controles, text="Limpiar", command=self.limpiar,
        ).pack(side="right", padx=(8, 4), pady=8)

        panel_gramatica = crear_superficie(self)
        panel_gramatica.pack(fill="both", expand=True, padx=34, pady=(0, 14))
        tk.Label(
            panel_gramatica, text="Gramática cargada",
            anchor="w", font=("Segoe UI", 12, "bold"),
            bg=COLORES["superficie"], fg=COLORES["texto"],
        ).pack(fill="x", padx=16, pady=(14, 8))
        self._crear_editor(panel_gramatica)

        self.estado_var = tk.StringVar(value="Listo para cargar una gramática.")
        tk.Label(
            self, textvariable=self.estado_var, anchor="w",
            font=("Segoe UI", 9), bg=COLORES["fondo"],
            fg=COLORES["secundario"],
        ).pack(fill="x", padx=36, pady=(0, 14))

    def _crear_editor(self, padre):
        contenedor = tk.Frame(padre, bg=COLORES["superficie"])
        contenedor.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.numeros_linea = tk.Text(
            contenedor, width=5, wrap="none", state="disabled",
            font=("Consolas", 10), bg=COLORES["superficie_alt"],
            fg=COLORES["secundario"], relief="flat", padx=6, pady=10,
            takefocus=0,
        )
        self.txt_gramatica = tk.Text(
            contenedor, wrap="none", state="disabled",
            font=("Consolas", 10), bg=COLORES["superficie_alt"],
            fg=COLORES["texto"], relief="flat", padx=12, pady=10,
        )
        scroll_y = ttk.Scrollbar(
            contenedor, orient="vertical", command=self._scroll_vertical
        )
        scroll_x = ttk.Scrollbar(
            contenedor, orient="horizontal", command=self.txt_gramatica.xview
        )
        self.txt_gramatica.configure(
            yscrollcommand=lambda a, b: self._actualizar_scroll(a, b, scroll_y),
            xscrollcommand=scroll_x.set,
        )
        self.numeros_linea.grid(row=0, column=0, sticky="ns")
        self.txt_gramatica.grid(row=0, column=1, sticky="nsew")
        scroll_y.grid(row=0, column=2, sticky="ns")
        scroll_x.grid(row=1, column=1, sticky="ew")
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)
        self._actualizar_numeros_linea()

    def _scroll_vertical(self, *args):
        self.txt_gramatica.yview(*args)
        self.numeros_linea.yview(*args)

    def _actualizar_scroll(self, primero, ultimo, scroll):
        scroll.set(primero, ultimo)
        self.numeros_linea.yview_moveto(primero)

    def _actualizar_numeros_linea(self):
        total = int(self.txt_gramatica.index("end-1c").split(".")[0])
        contenido = "\n".join(str(linea) for linea in range(1, total + 1))
        self.numeros_linea.configure(state="normal")
        self.numeros_linea.delete("1.0", tk.END)
        self.numeros_linea.insert("1.0", contenido)
        self.numeros_linea.configure(state="disabled")

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de gramática",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
        )
        if not ruta:
            return
        try:
            gramatica = cargar_gramatica_desde_archivo(ruta)
        except (OSError, UnicodeError, ValueError) as error:
            messagebox.showerror("No se pudo cargar la gramática", str(error))
            return

        self.ruta_actual = ruta
        self.gramatica = gramatica
        self.ruta_var.set(ruta)
        self._mostrar_gramatica()
        self.estado_var.set("Gramática cargada. Presiona «Analizar» para comenzar.")

    def _mostrar_gramatica(self):
        lineas = [
            "Terminales: " + " ".join(self.gramatica.terminales),
            "No terminales: " + " ".join(self.gramatica.no_terminales),
            "",
        ]
        for cabeza, cuerpos in self.gramatica.producciones.items():
            for cuerpo in cuerpos:
                lineas.append(f"{cabeza} -> {' '.join(cuerpo)}")

        self.txt_gramatica.configure(state="normal")
        self.txt_gramatica.delete("1.0", tk.END)
        self.txt_gramatica.insert("1.0", "\n".join(lineas))
        self.txt_gramatica.configure(state="disabled")
        self._actualizar_numeros_linea()

    def analizar(self):
        if not self.gramatica:
            messagebox.showinfo("Gramática requerida", "Primero selecciona una gramática.")
            return
        try:
            primeros = {}
            for no_terminal in self.gramatica.no_terminales:
                calcular_primeros(
                    no_terminal, self.gramatica.producciones, primeros,
                    self.gramatica.terminales,
                )

            siguientes = {nt: set() for nt in self.gramatica.no_terminales}
            for no_terminal in self.gramatica.no_terminales:
                calcular_siguientes(
                    no_terminal, self.gramatica.producciones, primeros,
                    siguientes, self.gramatica.simbolo_inicial,
                    self.gramatica.terminales,
                )
        except (KeyError, RecursionError, ValueError) as error:
            messagebox.showerror("Error durante el análisis", str(error))
            return

        if self.ventana_resultados and self.ventana_resultados.winfo_exists():
            self.ventana_resultados.destroy()
        primeros_salida = {
            nt: primeros.get(nt, set()) for nt in self.gramatica.no_terminales
        }
        siguientes_salida = {
            nt: siguientes.get(nt, set()) for nt in self.gramatica.no_terminales
        }
        if self.ventana_resultados and self.ventana_resultados.winfo_exists():
            self.ventana_resultados.destroy()
        self.ventana_resultados = VentanaPrimerosSiguientes(
            self, primeros_salida, siguientes_salida
        )
        self.estado_var.set(
            f"Análisis terminado: {len(primeros_salida)} no terminales procesados."
        )

    def limpiar(self):
        self.ruta_actual = ""
        self.gramatica = None
        self.ruta_var.set("Ningún archivo seleccionado")
        self.txt_gramatica.configure(state="normal")
        self.txt_gramatica.delete("1.0", tk.END)
        self.txt_gramatica.configure(state="disabled")
        self._actualizar_numeros_linea()
        self.estado_var.set("Listo para cargar una gramática.")


if __name__ == "__main__":
    InterfazCompilador().mainloop()
