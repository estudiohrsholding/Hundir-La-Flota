# barco.py

class Barco:
    """
    Representa un único barco en el juego.
    """
    def __init__(self, eslora):
        """
        Inicializa un barco con una eslora (tamaño) dada.

        Args:
            eslora (int): El tamaño del barco.
        """
        self.eslora = eslora
        self.posicion = []  # Lista de tuplas (x, y)
        self.impactos = set()  # Conjunto de tuplas (x, y) para los impactos recibidos

    def esta_hundido(self):
        """
        Verifica si el barco ha sido completamente hundido.

        Returns:
            bool: True si el número de impactos es igual a la eslora, False en caso contrario.
        """
        return len(self.impactos) == self.eslora
