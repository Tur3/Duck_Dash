"""
Controlli tastiera per test
"""
from kivy.core.window import Window
import config


class KeyboardControl:
    """Controllo manuale parametri via tastiera."""
    
    def __init__(self, simulator):
        self.sim = simulator
        self._keyboard = Window.request_keyboard(None, None)
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_key)
    
    def _on_key(self, keyboard, keycode, text, modifiers):
        """Gestisce tasti."""
        key = keycode[1]
        
        # Velocità
        if key == 'up':
            self.sim._speed = min(self.sim._speed + 10, config.MAX_SPEED)
        elif key == 'down':
            self.sim._speed = max(self.sim._speed - 10, 0)
        
        # RPM
        elif key == 'r':
            self.sim._rpm = min(self.sim._rpm + 500, config.MAX_RPM)
        elif key == 'f':
            self.sim._rpm = max(self.sim._rpm - 500, 800)
        
        # Preset
        elif key == '1':  # Idle
            self.sim._speed = 0
            self.sim._rpm = 800
        elif key == '2':  # Città
            self.sim._speed = 50
            self.sim._rpm = 2000
        elif key == '3':  # Autostrada
            self.sim._speed = 130
            self.sim._rpm = 3000
        elif key == '4':  # Sport
            self.sim._speed = 180
            self.sim._rpm = 6000
        
        # Ferma simulazione auto
        if key in ['1', '2', '3', '4']:
            self.sim._target_speed = self.sim._speed
        
        return True
