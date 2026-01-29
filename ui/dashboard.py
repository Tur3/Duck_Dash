"""
Dashboard widget
"""
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import config


class Dashboard(FloatLayout):
    """Widget dashboard principale."""
    
    def __init__(self, simulator, **kwargs):
        super().__init__(**kwargs)
        self.sim = simulator
        Clock.schedule_interval(self.update, config.UPDATE_INTERVAL)
    
    def update(self, dt):
        """Aggiorna dati dashboard."""
        data = self.sim.get_data()
        
        # Aggiorna RPM
        self.ids.rpm_value.text = str(int(data['rpm']))
        
        # Colore RPM
        if data['rpm'] >= config.REDLINE_RPM:
            self.ids.rpm_value.color = config.COLOR_RED
        elif data['rpm'] >= config.WARNING_RPM:
            self.ids.rpm_value.color = config.COLOR_YELLOW
        else:
            self.ids.rpm_value.color = config.COLOR_WHITE
        
  	# Aggiorna velocità (km/h)
        self.ids.speed_value.text = str(int(data['speed']))  # Questo aggiorna il label della velocità

        # Aggiorna barre
        self._update_bar('temp_bar', data['temp'], config.MAX_TEMP)
        self._update_bar('temp_oil_bar', data['temp_oil'], config.MAX_TEMP + 20)
        self._update_bar('fuel_bar', data['fuel'], 100)
    
    def _update_bar(self, bar_id, value, max_value):
        """Aggiorna barra progresso."""
        bar = self.ids[bar_id]
        progress = min(value / max_value, 1.0)
        bar.size_hint_x = progress
        
        # Colore barra
        bar.canvas.before.clear()
        with bar.canvas.before:
            # Determina colore
            if bar_id == 'fuel_bar':
                if value < config.WARNING_FUEL:
                    Color(*config.COLOR_RED)
                elif value < config.WARNING_FUEL * 2:
                    Color(*config.COLOR_YELLOW)
                else:
                    Color(*config.COLOR_GREEN)
            else:  # Temperature
                if value >= config.CRITICAL_TEMP:
                    Color(*config.COLOR_RED)
                elif value >= config.WARNING_TEMP:
                    Color(*config.COLOR_YELLOW)
                else:
                    Color(*config.COLOR_GREEN)
            
            Rectangle(pos=bar.pos, size=bar.size)
