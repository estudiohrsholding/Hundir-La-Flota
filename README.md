🚢 Batalla Naval (Hundir la Flota) - Refactorización OOP
Este repositorio contiene el proyecto "Hundir la Flota" desarrollado en Python. La arquitectura ha sido refactorizada desde un enfoque procedural a una arquitectura de Programación Orientada a Objetos (OOP) y utiliza Pygame para la interfaz gráfica de usuario (GUI).

🚀 Instalación y Configuración
Para ejecutar este proyecto, no solo necesitas descargar el código, sino también instalar las dependencias de sistema (bibliotecas C) que Pygame requiere para compilarse y funcionar correctamente.

1. Clonar el Repositorio
Bash

git clone https://github.com/estudiohrsholding/batalla-naval-proyecto.git |
 cd batalla-naval-proyecto
(Reemplaza la URL si la de tu repositorio es diferente)

2. Crear y Activar un Entorno Virtual
Es una práctica estándar de Python aislar las dependencias del proyecto.

Bash

# 1. Crear el entorno
python3 -m venv .venv

# 2. Activar el entorno (macOS/Linux)
source .venv/bin/activate
(Para Windows, el comando de activación es: .\.venv\Scripts\activate)

3. Instalar Dependencias del Sistema (El "Hotfix")
¡Paso Crítico! Pygame es un wrapper (envoltorio) para las bibliotecas multimedia de C llamadas SDL. Si no tienes estas bibliotecas, la instalación de pip (Paso 4) fallará con errores como fatal error: 'SDL.h' file not found.

Para macOS (con Homebrew)
(Este es el fix que aplicamos):

Bash

brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi
Para Linux (Debian/Ubuntu)
Bash

sudo apt-get install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev
Para Windows
Windows generalmente descarga wheels pre-compilados de Pygame, por lo que este paso no suele ser necesario. Si la instalación de pip falla, deberás instalar las bibliotecas de SDL manualmente.

4. Instalar las Dependencias de Python
Una vez que las bibliotecas C están en tu sistema, instala pygame usando el archivo requirements.txt:

Bash

# (Asegúrate de que tu .venv esté activado)
pip install -r requirements.txt
(Si pip falla, intenta desinstalar versiones anteriores y limpiar la caché antes de reinstalar):

Bash

pip uninstall pygame
pip cache purge
pip install -r requirements.txt
🎮 Cómo Jugar
Una vez que el entorno virtual esté activado y las dependencias estén instaladas, ejecuta el main.py para iniciar el juego:

Bash

python3 main.py
Se abrirá una nueva ventana de Pygame con el juego.

🌳 Estructura del Proyecto (Arquitectura OOP)
main.py: Contiene la clase Juego(), que es el orquestador principal y el bucle de eventos de Pygame.

tablero.py: Contiene la clase Tablero(). Gestiona el estado de la cuadrícula, la colocación de barcos y la lógica de recibir_disparo().

jugador.py: Contiene las clases Jugador(), JugadorHumano() y JugadorMaquina().

barco.py: Contiene la clase Barco() (aún no implementada por "Jules", pero parte del plan).

constants.py: (Aún no implementado por "Jules", pero parte del plan).

requirements.txt: Lista las dependencias de Python (ej. pygame).
