#!/usr/bin/env python3
"""
Duck_Dash
Strumentazione digitale per veicoli
"""
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from core.simulator import DataSimulator
from core.keyboard import KeyboardControl
from ui.dashboard import Dashboard
import config

# Configurazione finestra FISSA
Config.set('graphics', 'width', str(config.SCREEN_WIDTH))
Config.set('graphics', 'height', str(config.SCREEN_HEIGHT))
Config.set('graphics', 'resizable', '0')  # NON ridimensionabile
Config.set('kivy', 'exit_on_escape', '1')


class Duck_Dash(App):
    """Applicazione dashboard."""
    
    def build(self):
        self.title = "Duck_Dash"
        
        # Carica layout
        Builder.load_file('ui/dashboard.kv')
        
	# Crea sorgente dati (simulatore o OBD2)
        if config.DEMO_MODE:
            from core.simulator import DataSimulator
            self.sim = DataSimulator()
            print("Modalità DEMO - Dati simulati")
        else:
            from core.obd_reader import OBDReader
            self.sim = OBDReader()

            if not self.sim.connect():
                print("OBD2 non disponibile - Fallback a DEMO")
                from core.simulator import DataSimulator
                self.sim = DataSimulator()
            else:
                print("Modalità OBD2 - Dati reali dal veicolo")

        # Crea dashboard
        dashboard = Dashboard(self.sim)
        
        # Abilita controlli tastiera
        if config.KEYBOARD_CONTROL:
            self.keyboard = KeyboardControl(self.sim)
            print("\n Controlli tastiera attivi:")
            print("  ↑/↓     = Velocità ±10 km/h")
            print("  ↑/↓     = RPM ±500")
            print("  1-4     = Preset (Idle/Città/Autostrada/Sport)")
            print("  ESC     = Esci\n")
        
        return dashboard


if __name__ == '__main__':
    Duck_Dash().run()
