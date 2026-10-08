"""Cálculo iterativo de los conjuntos PRIMERO."""


def calcular_primeros(simbolo, producciones, primeros, terminales):
    """Calcula PRIMERO para todos los símbolos hasta alcanzar un punto fijo."""
    no_terminales = set(producciones)
    no_terminales.update(
        simbolo for simbolo in primeros
        if simbolo not in terminales and simbolo not in {"ε", "$"}
    )

    primeros.setdefault("ε", {"ε"})
    for terminal in terminales:
        primeros.setdefault(terminal, {terminal})
    for no_terminal in no_terminales:
        primeros.setdefault(no_terminal, set())

    cambio = True
    while cambio:
        cambio = False
        for cabeza, reglas in producciones.items():
            for regla in reglas:
                nuevos = set()
                todos_derivan_epsilon = True

                if not regla or regla == ["ε"]:
                    nuevos.add("ε")
                else:
                    for elemento in regla:
                        conjunto = primeros.setdefault(
                            elemento,
                            {elemento} if elemento not in producciones else set(),
                        )
                        nuevos.update(conjunto - {"ε"})
                        if "ε" not in conjunto:
                            todos_derivan_epsilon = False
                            break
                    if todos_derivan_epsilon:
                        nuevos.add("ε")

                antes = len(primeros[cabeza])
                primeros[cabeza].update(nuevos)
                cambio |= len(primeros[cabeza]) != antes

    if simbolo in terminales or simbolo == "$":
        return {simbolo}
    if simbolo == "ε":
        return {"ε"}
    return primeros.setdefault(simbolo, set())
