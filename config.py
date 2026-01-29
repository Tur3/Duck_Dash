"""
Configurazione Duck_Dash
"""

# === MODALITÀ ===
DEMO_MODE = True  # True = simulazione, False = hardware OBD2

# === DISPLAY (FISSO - non ridimensionabile) ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# === AGGIORNAMENTO ===
UPDATE_INTERVAL = 0.1  # secondi (10 Hz)

# === LIMITI STRUMENTI ===
MAX_RPM = 8000
MAX_SPEED = 250
MAX_TEMP = 120

# === WARNING ===
WARNING_RPM = 6500
REDLINE_RPM = 7000
WARNING_TEMP = 100
CRITICAL_TEMP = 110
WARNING_FUEL = 15

# === COLORI ===
COLOR_BACKGROUND = (0, 0, 0, 1)  # Nero
COLOR_WHITE = (1, 1, 1, 1)
COLOR_GREEN = (0, 1, 0, 1)
COLOR_YELLOW = (1, 1, 0, 1)
COLOR_RED = (1, 0, 0, 1)
COLOR_GRAY = (0.5, 0.5, 0.5, 1)

# === CONTROLLI TASTIERA ===
KEYBOARD_CONTROL = True  # Abilita controlli manuali

# === OBD2 (quando DEMO_MODE = False) ===
OBD_PORT = '/dev/ttyUSB0'  # Windows: 'COM3'
