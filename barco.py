# barco.py

class Barco:
    """
    Representa un barco 'inteligente' que conoce su propio nombre, posición,
    orientación y estado.
    """
    def __init__(self, eslora, nombre):
        """
        Inicializa un barco con nombre y eslora.
        Args:
            eslora (int): El tamaño (longitud) del barco.
            nombre (str): El nombre del tipo de barco (ej: 'barco_6').
        """
        self.nombre = nombre
        self.eslora = eslora
        self.x = 0
        self.y = 0
        self.orientacion = 'h'
        self.impactos = set()  # Un conjunto de tuplas (x, y) para los impactos
        self.posicion = []

    def get_parte_en_coord(self, x, y):
        """
        Determina qué parte del barco (cabeza, cuerpo, cola) se encuentra
        en una coordenada específica.

        Returns:
            str: "CABEZA", "MEDIO", "COLA", o None.
        """
        if (x, y) not in self.posicion:
            return None

        if self.eslora == 1:
            return "UNICO"

        try:
            # La posición en la lista de coordenadas nos da el índice
            idx = self.posicion.index((x, y))
            if idx == 0:
                return "CABEZA"
            elif idx == self.eslora - 1:
                return "COLA"
            else:
                return "MEDIO"
        except ValueError:
            return None


    def recibir_impacto(self, x, y):
        """
        Registra un impacto en una coordenada específica del barco.
        """
        if (x, y) in self.posicion:
            self.impactos.add((x, y))
            return True
        return False

    def esta_hundido(self):
        """
        Verifica si el barco ha sido completamente hundido.
        """
        return len(self.impactos) == self.eslora
