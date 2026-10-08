"""Cálculo iterativo de los conjuntos SIGUIENTE."""


def _primero_secuencia(secuencia, primeros):
    """Devuelve PRIMERO de una secuencia y si toda ella deriva en ε."""
    resultado = set()
    toda_nula = True
    for simbolo in secuencia:
        conjunto = primeros.get(simbolo, {simbolo})
        resultado.update(conjunto - {"ε"})
        if "ε" not in conjunto:
            toda_nula = False
            break
    return resultado, toda_nula


def calcular_siguientes(
    no_terminal, producciones, primeros, siguientes, simbolo_inicial, terminales
):
    """Calcula SIGUIENTE para todos los no terminales hasta alcanzar un punto fijo."""
    del terminales
    for cabeza in producciones:
        siguientes.setdefault(cabeza, set())
    siguientes.setdefault(simbolo_inicial, set()).add("$")

    cambio = True
    while cambio:
        cambio = False
        for cabeza, reglas in producciones.items():
            for regla in reglas:
                for indice, simbolo in enumerate(regla):
                    if simbolo not in producciones:
                        continue

                    beta = regla[indice + 1:]
                    primeros_beta, beta_nula = _primero_secuencia(beta, primeros)
                    destino = siguientes[simbolo]
                    antes = len(destino)
                    destino.update(primeros_beta)
                    if beta_nula:
                        destino.update(siguientes[cabeza])
                    cambio |= len(destino) != antes

    return siguientes.get(no_terminal, set())
