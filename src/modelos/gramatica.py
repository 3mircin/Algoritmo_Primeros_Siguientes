class Gramatica:
    def __init__(self):
        self.terminales = []
        self.no_terminales = []
        self.simbolo_inicial = ""
        self.producciones = {}

    def agregar_produccion(self, cabeza, cuerpo):
        if cabeza not in self.producciones:
            self.producciones[cabeza] = []
        self.producciones[cabeza].append(cuerpo)