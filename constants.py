# constants.py

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
MARCADOR_FALLO = "FALLO_MARCADO"

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
    'agua': 'assets/images/Agua.png',
    'fallo': 'assets/images/fail_shoot.png',
    'impacto': 'assets/images/well_shoot.png',
    'barco_6': 'assets/images/piezas_6.png',
    'barco_5': 'assets/images/piezas_5.png',
    'barco_4': 'assets/images/piezas_4.png',
    'barco_3': 'assets/images/piezas_3.png',
    'barco_2': 'assets/images/piezas_2.png',
    'barco_1': 'assets/images/piezas_1.png'
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
