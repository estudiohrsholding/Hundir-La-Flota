# constants.py
import os

# Get the absolute path of the directory containing this file (constants.py)
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==============================================================================
# --- GENERALES ---
# ==============================================================================
TAMANO_TABLERO = 10

# ==============================================================================
# --- ESTADOS DEL Juego ---
# ==============================================================================
ESTADO_FALLO = "FALLO"
ESTADO_IMPACTO = "IMPACTO"
ESTADO_HUNDIDO = "HUNDIDO"
ESTADO_REPETIDO = "REPETIDO"

# ==============================================================================
# --- MARCADORES INTERNOS DE LA GRID (NO VISUALES) ---
# ==============================================================================
AGUA = None
MARCADOR_FALLO = "FALLO_MARCADO" # Usado internamente, la vista usará el sprite 'fallo'

# ==============================================================================
# --- CONSTANTES GRÁFICAS (Pygame) ---
# ==============================================================================

# --- Colores ---
COLOR_TEXTO = (255, 255, 255)
COLOR_FONDO = (0, 0, 0)

# --- Dimensiones ---
TAMANO_CELDA = 40
MARGEN_CELDA = 5

TAMANO_TABLERO_PX = 10 * (TAMANO_CELDA + MARGEN_CELDA)
ANCHO_VENTANA = (2 * TAMANO_TABLERO_PX) + (3 * TAMANO_CELDA)
ALTO_VENTANA = TAMANO_TABLERO_PX + (2 * TAMANO_CELDA)

# --- Rutas de los Assets ---
ASSETS = {
    'agua': os.path.join(_BASE_DIR, 'assets', 'images', 'Agua.png'),
    'fallo': os.path.join(_BASE_DIR, 'assets', 'images', 'fail_shoot.png'),
    'impacto': os.path.join(_BASE_DIR, 'assets', 'images', 'well_shoot.png'),
    'barco_6': os.path.join(_BASE_DIR, 'assets', 'images', 'piezas_6.png'),
    'barco_5': os.path.join(_BASE_DIR, 'assets', 'images', 'piezas_5.png'),
    'barco_4': os.path.join(_BASE_DIR, 'assets', 'images', 'piezas4.png'),
    'barco_3': os.path.join(_BASE_DIR, 'assets', 'images', 'piezas_3.png'),
    'barco_2': os.path.join(_BASE_DIR, 'assets', 'images', 'piezas_2.png'),
    'barco_1': os.path.join(_BASE_DIR, 'assets', 'images', 'piezas_1.png')
}

# La lista de barcos ahora es una lista de tuplas (nombre, eslora)
LISTA_BARCOS = [
    ('barco_6', 6),
    ('barco_5', 5),
    ('barco_4', 4),
    ('barco_3', 3),
    ('barco_2', 2),
    ('barco_1', 1)
]
