"""
Simulatore dati veicolo
"""
import time
import random
import config


class DataSimulator:
    """Genera dati realistici per demo."""
    
    def __init__(self):
        self._speed = 0
        self._rpm = 800
        self._temp = 20
        self._temp_oil = 20
        self._fuel = 75
        self._target_speed = 0
        self._last_update = time.time()
    
    def get_data(self):
        """Aggiorna e restituisce tutti i dati."""
        current_time = time.time()
        dt = current_time - self._last_update
        self._last_update = current_time
        
        # Aggiorna comportamento
        self._update_driving(dt)
        self._update_rpm()
        self._update_temps(dt)
        self._update_fuel(dt)
        
        return {
            'speed': round(self._speed, 1),
            'rpm': int(self._rpm),
            'temp': round(self._temp, 1),
            'temp_oil': round(self._temp_oil, 1),
            'fuel': round(self._fuel, 1)
        }
    
    def _update_driving(self, dt):
        """Simula accelerazione/frenata."""
        # Cambia target casualmente
        if random.random() < 0.02:
            self._target_speed = random.uniform(0, config.MAX_SPEED * 0.6)
        
        # Aggiorna velocità verso target
        diff = self._target_speed - self._speed
        if abs(diff) > 1:
            accel = min(10.0, diff * 0.5) if diff > 0 else max(-15.0, diff * 0.5)
            self._speed += accel * dt
            self._speed = max(0, min(config.MAX_SPEED, self._speed))
    
    def _update_rpm(self):
        """Calcola RPM in base a velocità."""
        if self._speed < 5:
            self._rpm = 800 + random.uniform(-50, 50)
        else:
            # Simula marce
            if self._speed < 20:
                ratio = 180
            elif self._speed < 40:
                ratio = 100
            elif self._speed < 70:
                ratio = 65
            elif self._speed < 100:
                ratio = 45
            else:
                ratio = 30
            
            self._rpm = self._speed * ratio + random.uniform(-100, 100)
            self._rpm = max(800, min(config.MAX_RPM, self._rpm))
    
    def _update_temps(self, dt):
        """Aggiorna temperature."""
        # Temperatura acqua
        target_temp = 90 if self._rpm > 2000 else 85
        diff = target_temp - self._temp
        self._temp += diff * 0.3 * dt
        self._temp = max(20, min(config.MAX_TEMP, self._temp))
        
        # Temperatura olio (più alta)
        self._temp_oil = self._temp + 10 + (self._rpm / 1000)
        self._temp_oil = max(20, min(config.MAX_TEMP + 20, self._temp_oil))
    
    def _update_fuel(self, dt):
        """Simula consumo."""
        consumption = (self._rpm / 10000) * 0.05 * dt
        self._fuel -= consumption
        if self._fuel < 5:
            self._fuel = 100  # Rifornimento auto
