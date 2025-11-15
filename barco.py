# barco.py

class Barco:
    """
    Representa un barco 'inteligente' que conoce su propio nombre, posición,
    orientación y estado.
    """
    def __init__(self, nombre, eslora, x, y, orientacion):
        """
        Inicializa un barco con nombre, eslora, posición y orientación.
        Args:
            nombre (str): El nombre del tipo de barco (ej: 'portaaviones').
            eslora (int): El tamaño (longitud) del barco.
            x (int): La coordenada X de la proa (cabeza) del barco.
            y (int): La coordenada Y de la proa (cabeza) del barco.
            orientacion (str): "H" para horizontal, "V" para vertical.
        """
        self.nombre = nombre
        self.eslora = eslora
        self.x = x
        self.y = y
        self.orientacion = orientacion
        self.impactos = set()  # Un conjunto de tuplas (x, y) para los impactos

    @property
    def coordenadas(self):
        """
        Calcula y devuelve todas las coordenadas que ocupa el barco.
        Es una property para que se calcule dinámicamente.
        """
        coords = []
        if self.orientacion == "H":
            for i in range(self.eslora):
                coords.append((self.x + i, self.y))
        else: # "V"
            for i in range(self.eslora):
                coords.append((self.x, self.y + i))
        return coords

    def get_parte_en_coordenada(self, cx, cy):
        """
        Determina qué parte del barco (cabeza, cuerpo, cola) se encuentra
        en una coordenada específica.

        Returns:
            str: "CABEZA", "CUERPO", "COLA", "UNICO", o None.
        """
        if (cx, cy) not in self.coordenadas:
            return None

        if self.eslora == 1:
            return "UNICO"

        try:
            # La posición en la lista de coordenadas nos da el índice
            idx = self.coordenadas.index((cx, cy))
            if idx == 0:
                return "CABEZA"
            elif idx == self.eslora - 1:
                return "COLA"
            else:
                return "CUERPO"
        except ValueError:
            return None


    def recibir_impacto(self, x, y):
        """
        Registra un impacto en una coordenada específica del barco.
        """
        if (x, y) in self.coordenadas:
            self.impactos.add((x, y))
            return True
        return False

    def esta_hundido(self):
        """
        Verifica si el barco ha sido completamente hundido.
        """
        return len(self.impactos) == self.eslora
