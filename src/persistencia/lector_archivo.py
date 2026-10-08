# src/persistencia/lector_archivo.py
from modelos.gramatica import Gramatica

def cargar_gramatica_desde_archivo(ruta_archivo):
    """
    Lee un archivo txt y retorna un objeto Gramatica.
    Se espera el formato:
    - Producciones, una por línea (ej. ``D -> T id L ;``).
      Los terminales y no terminales se infieren automáticamente.
    - También se acepta el formato anterior con terminales en la primera
      línea y no terminales en la segunda.
    """
    gramatica = Gramatica()

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        lineas = [linea.strip() for linea in archivo if linea.strip()]

    if not lineas:
        raise ValueError("El archivo no tiene el formato correcto.")

    # Si las dos primeras líneas no son producciones, son encabezados.
    tiene_encabezados = (
        len(lineas) >= 3
        and not ("->" in lineas[0] or "→" in lineas[0])
        and not ("->" in lineas[1] or "→" in lineas[1])
    )
    producciones = lineas[2:] if tiene_encabezados else lineas
    if tiene_encabezados:
        gramatica.terminales = lineas[0].split()
        gramatica.no_terminales = lineas[1].split()

    for linea in producciones:
        if '->' in linea:
            cabeza, cuerpo_str = linea.split('->', 1)
        elif '→' in linea:
            cabeza, cuerpo_str = linea.split('→', 1)
        else:
            raise ValueError(f"Producción inválida: {linea}")

        cabeza = cabeza.strip()
        if not cabeza:
            raise ValueError(f"Producción sin no terminal: {linea}")
        cuerpo = cuerpo_str.strip().split() or ['ε']

        if len(cuerpo) == 1 and cuerpo[0].lower() in {'epsilon', 'e', 'ε'}:
            cuerpo = ['ε']

        gramatica.agregar_produccion(cabeza, cuerpo)

    if not gramatica.producciones:
        raise ValueError("El archivo no contiene producciones.")

    if not gramatica.no_terminales:
        gramatica.no_terminales = list(gramatica.producciones)
    else:
        faltantes = set(gramatica.producciones) - set(gramatica.no_terminales)
        if faltantes:
            raise ValueError(
                "No terminales no declarados: " + ", ".join(sorted(faltantes))
            )

    simbolos_rhs = {
        simbolo
        for reglas in gramatica.producciones.values()
        for regla in reglas
        for simbolo in regla
        if simbolo != "ε"
    }
    if not gramatica.terminales:
        gramatica.terminales = sorted(
            simbolos_rhs - set(gramatica.no_terminales)
        )

    gramatica.simbolo_inicial = gramatica.no_terminales[0]
    return gramatica