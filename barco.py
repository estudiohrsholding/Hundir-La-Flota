# barco.py

class Barco:
    """
    Representa un barco 'inteligente' que conoce su propia posición,
    orientación y estado.
    """
    def __init__(self, eslora, x, y, orientacion):
        """
        Inicializa un barco con eslora, posición y orientación.

        Args:
            eslora (int): El tamaño (longitud) del barco.
            x (int): La coordenada X de la proa (cabeza) del barco.
            y (int): La coordenada Y de la proa (cabeza) del barco.
            orientacion (str): "H" para horizontal, "V" para vertical.
        """
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
        Determina qué parte del barco (proa, popa, cuerpo) se encuentra
        en una coordenada específica.

        Args:
            cx (int): Coordenada X a verificar.
            cy (int): Coordenada Y a verificar.

        Returns:
            str: "PROA", "POPA", "CUERPO", "UNICO", o None si el barco no está en (cx, cy).
        """
        if (cx, cy) not in self.coordenadas:
            return None

        if self.eslora == 1:
            return "UNICO"

        idx = -1
        if self.orientacion == "H":
            idx = cx - self.x
        else: # "V"
            idx = cy - self.y

        if idx == 0:
            return "PROA"
        elif idx == self.eslora - 1:
            return "POPA"
        else:
            return "CUERPO"

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

        Returns:
            bool: True si el número de impactos es igual a la eslora, False en caso contrario.
        """
        return len(self.impactos) == self.eslora
