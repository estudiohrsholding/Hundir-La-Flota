# constants.py

# ==============================================================================
# --- GENERALES ---
# ==============================================================================
TAMANO_TABLERO = 10

# La lista de barcos ahora es una lista de tuplas (eslora, nombre)
# para poder cargar los assets correspondientes.
LISTA_BARCOS = [
    (5, 'portaaviones'),
    (4, 'acorazado'),
    (3, 'submarino'),
    (3, 'destructor'),
    (2, 'patrullero'),
    (2, 'bote')
]

# ==============================================================================
# --- ESTADOS DEL JUEGO ---
# ==============================================================================
# Estos estados son devueltos por `recibir_disparo` para comunicar el resultado.
ESTADO_FALLO = "FALLO"
ESTADO_IMPACTO = "IMPACTO"
ESTADO_HUNDIDO = "HUNDIDO"
ESTADO_REPETIDO = "REPETIDO"

# ==============================================================================
# --- MARCADORES INTERNOS DE LA GRID (NO VISUALES) ---
# ==============================================================================
# La grid puede contener 'AGUA' o un objeto Barco.
# Cuando se dispara, el estado de la celda puede cambiar a un marcador.
AGUA = None
MARCADOR_FALLO = "FALLO_MARCADO" # Marcador para un tiro fallado
# El impacto se gestiona en el propio objeto Barco, no con un marcador en la grid.

# ==============================================================================
# --- CONSTANTES GRÁFICAS (Pygame) ---
# ==============================================================================

# --- Colores ---
COLOR_AGUA = (22, 100, 150)
COLOR_TEXTO = (255, 255, 255)
COLOR_FONDO = (0, 0, 0)

# --- Dimensiones ---
TAMANO_CELDA = 40  # Ancho y alto de cada celda en píxeles
MARGEN_CELDA = 5   # Espacio entre celdas en píxeles

# Cálculo del tamaño total de un tablero en píxeles
TAMANO_TABLERO_PX = TAMANO_TABLERO * (TAMANO_CELDA + MARGEN_CELDA)

# Cálculo del tamaño de la ventana
ANCHO_VENTANA = (2 * TAMANO_TABLERO_PX) + (3 * TAMANO_CELDA) # Dos tableros + margen central
ALTO_VENTANA = TAMANO_TABLERO_PX + (2 * TAMANO_CELDA)      # Tablero + márgenes superior/inferior

# --- Rutas de los Assets ---
ASSETS = {
    'agua': 'assets/images/agua.png',
    'fallo': 'assets/images/fallo.png',
    'impacto': 'assets/images/impacto.png',
    'portaaviones': 'assets/images/portaaviones_h.png',
    'acorazado': 'assets/images/acorazado_h.png',
    'submarino': 'assets/images/submarino_h.png',
    'destructor': 'assets/images/destructor_h.png',
    'patrullero': 'assets/images/patrullero_h.png',
    'bote': 'assets/images/bote_h.png'
}
