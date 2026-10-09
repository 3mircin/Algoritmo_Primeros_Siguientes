# Analizador de Primeros y Siguientes

Herramienta de escritorio en Python que calcula los conjuntos **PRIMERO (First)** y **SIGUIENTE (Follow)** de cualquier gramática libre de contexto, presentando los resultados en una interfaz gráfica limpia construida con Tkinter.

Desarrollado como proyecto del segundo parcial de la materia **Compiladores** — Universidad Tecnológica de la Mixteca (UTM), 5.° semestre.

---

## Tabla de contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Formato del archivo de gramática](#formato-del-archivo-de-gramática)
- [Archivos de prueba](#archivos-de-prueba)
- [Algoritmos implementados](#algoritmos-implementados)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Reporte](#reporte)
- [Capturas de pantalla](#capturas-de-pantalla)

---

## Descripción

En el diseño de compiladores, los conjuntos **PRIMERO** y **SIGUIENTE** son fundamentales para construir analizadores sintácticos predictivos (LL(1)). Esta herramienta automatiza ese cálculo:

- **PRIMERO(X)** — conjunto de terminales que pueden aparecer al inicio de cualquier cadena derivada desde el símbolo `X`. Si `X` puede derivar en la cadena vacía, también incluye `ε`.
- **SIGUIENTE(X)** — conjunto de terminales que pueden aparecer inmediatamente a la derecha de `X` en alguna forma sentencial. Incluye `$` si `X` puede ser el último símbolo de una derivación.

---

## Características

- Carga gramáticas desde archivos `.txt` con detección automática de terminales y no terminales.
- Soporta dos formatos de archivo: con encabezados explícitos o solo producciones.
- Acepta producciones vacías escritas como `ε`, `e` o `epsilon`.
- Calcula PRIMERO y SIGUIENTE mediante algoritmos iterativos de punto fijo.
- Muestra los resultados en una ventana con pestañas separadas para cada conjunto.
- Editor de solo lectura con numeración de líneas para inspeccionar la gramática cargada.
- Interfaz de modo claro con estilos coherentes en todos los componentes.

---

## Requisitos

- Python **3.10** o superior
- Tkinter (incluido en la instalación estándar de Python en Windows y macOS)

En Linux puede ser necesario instalarlo aparte:

```bash
# Debian / Ubuntu
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

No se requieren dependencias externas (sin `pip install`).

---

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/adrianarias2005-toexee/Algoritmo_Primeros_Siguientes.git
cd Algoritmo_Primeros_Siguientes

# 2. Ejecutar la interfaz
cd src
python interfaz.py
```

> En Windows también está disponible el ejecutable precompilado `AlgoritmoPrimerosSiguientes.exe` en la raíz del repositorio; no requiere Python instalado.

---

## Formato del archivo de gramática

El analizador acepta archivos `.txt` en dos formatos.

### Formato simple (recomendado)

Solo escribe las producciones, una por línea. Los terminales y no terminales se detectan automáticamente: cualquier símbolo que aparezca como cabeza de una producción es no terminal; el resto son terminales.

```
E -> T E'
E' -> + T E'
E' -> ε
T -> F T'
T' -> * F T'
T' -> ε
F -> ( E )
F -> id
```

### Formato con encabezados

Las primeras dos líneas declaran explícitamente los terminales y no terminales, y las producciones van a partir de la tercera línea.

```
+ * ( ) id
E E' T T' F
E -> T E'
E' -> + T E'
...
```

### Reglas generales

| Aspecto | Detalle |
|---|---|
| Separador de producción | `->` o `→` |
| Cadena vacía | `ε`, `e` o `epsilon` (sin distinción de mayúsculas) |
| Símbolos | Separados por espacios dentro del cuerpo de la producción |
| Símbolo inicial | Siempre el no terminal de la **primera** producción del archivo |
| Codificación | UTF-8 |
| Líneas en blanco | Se ignoran |

---

## Archivos de prueba

El directorio `ArchivosdePrueba/` contiene seis gramáticas listas para usar:

| Archivo | Gramática | Notas |
|---|---|---|
| `Gramatica1.txt` | Expresiones aritméticas con `+` y `*` | Contiene recursión izquierda |
| `Gramatica2.txt` | Declaraciones de variables `T id L ;` | Listas separadas por comas, L puede ser ε |
| `Gramatica3.txt` | Variante de declaraciones | El tipo `T` también puede ser ε |
| `Gramatica4.txt` | Sentencias: asignación, `print`, expresiones | Incluye recursión en `S` y `L` |
| `Gramatica5.txt` | Declaración de arreglos `T id[nint]` | Usa V' para la parte opcional |
| `Gramatica6.txt` | Expresiones sin recursión izquierda | Versión LL(1) de Gramática1 |

---

## Algoritmos implementados

### PRIMERO — algoritmo iterativo de punto fijo

Ubicado en `src/persistencia/algoritmo_primeros.py`.

1. Inicializar: `PRIMERO(a) = {a}` para cada terminal `a`; `PRIMERO(X) = {}` para cada no terminal.
2. Repetir hasta que no haya cambios:
   - Para cada producción `X → Y₁ Y₂ … Yₙ`:
     - Agregar `PRIMERO(Y₁) − {ε}` a `PRIMERO(X)`.
     - Si `ε ∈ PRIMERO(Y₁)`, agregar también `PRIMERO(Y₂) − {ε}`, y así sucesivamente.
     - Si todos los `Yᵢ` pueden derivar `ε`, agregar `ε` a `PRIMERO(X)`.
   - Para la producción `X → ε`, agregar `ε` a `PRIMERO(X)`.

### SIGUIENTE — algoritmo iterativo de punto fijo

Ubicado en `src/persistencia/algoritmo_siguientes.py`.

1. Inicializar: `SIGUIENTE(S) = {$}` donde `S` es el símbolo inicial; `SIGUIENTE(X) = {}` para los demás.
2. Repetir hasta que no haya cambios:
   - Para cada producción `A → α B β`:
     - Agregar `PRIMERO(β) − {ε}` a `SIGUIENTE(B)`.
     - Si `ε ∈ PRIMERO(β)` (o `β = ε`), agregar `SIGUIENTE(A)` a `SIGUIENTE(B)`.

---

## Estructura del proyecto

```
Algoritmo_Primeros_Siguientes/
│
├── AlgoritmoPrimerosSiguientes.exe   # Ejecutable para Windows
│
├── ArchivosdePrueba/                 # Gramáticas de ejemplo
│   ├── Gramatica1.txt
│   ├── Gramatica2.txt
│   ├── Gramatica3.txt
│   ├── Gramatica4.txt
│   ├── Gramatica5.txt
│   └── Gramatica6.txt
│
├── reporte/
│   └── informe/
│       ├── InformeActividadesEq1.tex # Documento principal LaTeX
│       ├── InformeActividadesEq1.pdf # PDF compilado
│       ├── secciones/
│       │   ├── portada.tex
│       │   ├── modelo.tex
│       │   ├── analisis.tex
│       │   ├── asignacion.tex
│       │   ├── clases_metodos.tex
│       │   ├── avances.tex
│       │   ├── conclusiones.tex
│       │   └── referencias.tex
│       └── imagenes/
│           ├── logo-utm.png
│           └── modelo_programa_principal.png
│
└── src/
    ├── interfaz.py                   # Punto de entrada — ventana principal
    │
    ├── modelos/
    │   └── gramatica.py              # Clase Gramatica (terminales, no terminales, producciones)
    │
    ├── persistencia/
    │   ├── lector_archivo.py         # Lectura y parseo del archivo .txt
    │   ├── algoritmo_primeros.py     # Cálculo de conjuntos PRIMERO
    │   └── algoritmo_siguientes.py   # Cálculo de conjuntos SIGUIENTE
    │
    └── presentacion/
        ├── estilos.py                # Paleta de colores y estilos ttk
        ├── tabla_base.py             # Widget Treeview reutilizable con scrollbars
        ├── tabla_conjuntos.py        # Tabla que muestra un conjunto por no terminal
        └── ventana_primeros_siguientes.py  # Ventana de resultados con pestañas
```

### Flujo de datos

```
Archivo .txt
    └─► lector_archivo.py  ──►  Gramatica
                                    ├─► algoritmo_primeros.py  ──►  {NT: set}
                                    └─► algoritmo_siguientes.py ──►  {NT: set}
                                                                          │
                                                            VentanaPrimerosSiguientes
                                                                ├── TablaConjuntos (Primeros)
                                                                └── TablaConjuntos (Siguientes)
```

---

## Reporte

El directorio `reporte/informe/` contiene el informe de actividades del proyecto escrito en LaTeX. El PDF compilado (`InformeActividadesEq1.pdf`) se incluye directamente en el repositorio.

Para recompilar el PDF desde las fuentes:

```bash
cd reporte/informe
pdflatex InformeActividadesEq1.tex
pdflatex InformeActividadesEq1.tex   # segunda pasada para referencias
```

> Requiere una distribución LaTeX instalada (TeX Live, MiKTeX o MacTeX).

El informe cubre las siguientes secciones:

| Sección | Descripción |
| --- | --- |
| Portada | Datos del equipo, materia y período |
| Índice | Tabla de contenidos generada automáticamente |
| Análisis | Algoritmo de Primero y Algoritmo de Siguiente (descripción formal) |
| Modelo del programa | Diagrama de clases y arquitectura en capas |
| Asignación de actividades | Distribución de tareas por sub equipo |
| Clases y módulos | Descripción técnica de cada módulo implementado |
| Avances | Tabla de avances diarios por integrante |
| Conclusiones | Reflexiones sobre el proceso y los resultados |
| Referencias | Bibliografía utilizada |

---

## Capturas de pantalla

> *Agrega aquí capturas de la ventana principal y de la ventana de resultados.*

---

## Integrantes

**Equipo 1 — Universidad Tecnológica de la Mixteca**

- Cortez Vega Jaime Fabian
- Carrasco Pacheco Levi Josue
- Arias Mendoza Angel Adrian
- Vazquez Moreno Zair de Jesus
- Nicolas Vazquez Joel Osmar
- Lujan de la Rosa Cristian Emir
