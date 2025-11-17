# clases.py
import numpy as np
import variables as var
import random

class Tablero:
    """
    Clase que gestiona el estado del tablero de un jugador en Batalla Naval.

    Atributos:
        id_jugador (str): Identificador del jugador ('Player' o 'AI').
        tablero_privado (np.array): Tablero 10x10 que contiene la posición real de los barcos.
        tablero_publico (np.array): Tablero 10x10 que muestra los resultados de los disparos del oponente.
        barcos (list): Lista con las esloras de los barcos a colocar.
    """
    def __init__(self, id_jugador):
        """
        Inicializa un objeto Tablero para un jugador específico.
        """
        self.id_jugador = id_jugador
        self.tablero_privado = np.full((var.TAMANO_TABLERO, var.TAMANO_TABLERO), var.AGUA)
        self.tablero_publico = np.full((var.TAMANO_TABLERO, var.TAMANO_TABLERO), var.AGUA)
        self.barcos = var.LISTA_BARCOS.copy()

    def inicializar_barcos(self):
        """
        Coloca los barcos de forma aleatoria en el tablero privado.
        """
        for eslora in self.barcos:
            colocado = False
            while not colocado:
                x = random.randint(0, var.TAMANO_TABLERO - 1)
                y = random.randint(0, var.TAMANO_TABLERO - 1)
                orientacion = random.choice(["H", "V"])

                if self._puede_colocar(x, y, eslora, orientacion):
                    self._colocar(x, y, eslora, orientacion)
                    colocado = True

    def _puede_colocar(self, x, y, eslora, orientacion):
        """
        Verifica si un barco se puede colocar en las coordenadas dadas sin solaparse.
        """
        if orientacion == "H":
            if x + eslora > var.TAMANO_TABLERO:
                return False
            return np.all(self.tablero_privado[y, x:x+eslora] == var.AGUA)
        else: # "V"
            if y + eslora > var.TAMANO_TABLERO:
                return False
            return np.all(self.tablero_privado[y:y+eslora, x] == var.AGUA)

    def _colocar(self, x, y, eslora, orientacion):
        """
        Coloca un barco en el tablero privado.
        """
        if orientacion == "H":
            self.tablero_privado[y, x:x+eslora] = var.BARCO
        else: # "V"
            self.tablero_privado[y:y+eslora, x] = var.BARCO

    def recibir_disparo(self, x, y):
        """
        Registra un disparo en el tablero y actualiza el estado.

        Devuelve:
            - True: Si es un impacto.
            - False: Si es agua.
            - None: Si la casilla ya había sido disparada.
        """
        casilla_actual = self.tablero_privado[y, x]

        if casilla_actual == var.BARCO:
            self.tablero_privado[y, x] = var.IMPACTO
            self.tablero_publico[y, x] = var.IMPACTO
            return True  # Impacto
        elif casilla_actual == var.AGUA:
            self.tablero_privado[y, x] = var.FALLO
            self.tablero_publico[y, x] = var.FALLO
            return False  # Agua
        elif casilla_actual in (var.IMPACTO, var.FALLO):
            return None  # Disparo repetido

    def comprobar_victoria(self):
        """
        Comprueba si todos los barcos del jugador han sido hundidos.

        Devuelve:
            - True: Si no quedan barcos a flote.
            - False: Si todavía quedan barcos.
        """
        return not np.any(self.tablero_privado == var.BARCO)

    def mostrar_tablero(self, tipo_vista='publico'):
        """
        Muestra el tablero en consola con un formato legible.
        """
        # Mapeo de valores numéricos a caracteres para visualización
        mapa_simbolos = {
            var.AGUA: "~",
            var.BARCO: "B",
            var.IMPACTO: "X",
            var.FALLO: "O"
        }

        tablero_a_mostrar = self.tablero_publico if tipo_vista == 'publico' else self.tablero_privado

        print(f"  {' '.join(map(str, range(var.TAMANO_TABLERO)))}") # Cabecera de columnas
        for i, fila in enumerate(tablero_a_mostrar):
            linea = f"{i} "
            for celda in fila:
                linea += f"{mapa_simbolos.get(celda, '?')} "
            print(linea.strip())
