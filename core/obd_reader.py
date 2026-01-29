"""
Lettore dati OBD2 reali da veicolo
"""
import obd
import config


class OBDReader:
    """Legge dati reali da porta OBD2."""
    
    def __init__(self):
        self.connection = None
        self._speed = 0
        self._rpm = 0
        self._temp = 0
        self._temp_oil = 0
        self._fuel = 0
    
    def connect(self):
        """Connette a porta OBD2."""
        try:
            print(f"[OBD2] Connessione a {config.OBD_PORT}...")
            
            self.connection = obd.OBD(config.OBD_PORT)
            
            if self.connection.is_connected():
                print(f"[OBD2] ✓ Connesso")
                print(f"[OBD2] Protocollo: {self.connection.protocol_name()}")
                return True
            else:
                print("[OBD2] ✗ Connessione fallita")
                print("  Verifica:")
                print("  - Adattatore OBD2 collegato")
                print("  - Porta corretta in config.py")
                print("  - Veicolo acceso (quadro ON)")
                return False
                
        except Exception as e:
            print(f"[OBD2] ✗ Errore: {e}")
            return False
    
    def get_data(self):
        """Legge dati da OBD2."""
        if not self.connection or not self.connection.is_connected():
            return self._get_zero_data()
        
        try:
            # Leggi velocità
            response = self.connection.query(obd.commands.SPEED)
            if not response.is_null():
                self._speed = response.value.magnitude
            
            # Leggi RPM
            response = self.connection.query(obd.commands.RPM)
            if not response.is_null():
                self._rpm = response.value.magnitude
            
            # Leggi temperatura refrigerante
            response = self.connection.query(obd.commands.COOLANT_TEMP)
            if not response.is_null():
                self._temp = response.value.magnitude
            
            # Temperatura olio (se supportato)
            response = self.connection.query(obd.commands.OIL_TEMP)
            if not response.is_null():
                self._temp_oil = response.value.magnitude
            else:
                # Stima da temp refrigerante
                self._temp_oil = self._temp + 10
            
            # Livello carburante
            response = self.connection.query(obd.commands.FUEL_LEVEL)
            if not response.is_null():
                self._fuel = response.value.magnitude
            
            return {
                'speed': round(self._speed, 1),
                'rpm': int(self._rpm),
                'temp': round(self._temp, 1),
                'temp_oil': round(self._temp_oil, 1),
                'fuel': round(self._fuel, 1)
            }
            
        except Exception as e:
            print(f"[OBD2] Errore lettura: {e}")
            return self._get_zero_data()
    
    def _get_zero_data(self):
        """Dati di default se OBD2 non connesso."""
        return {
            'speed': 0,
            'rpm': 0,
            'temp': 0,
            'temp_oil': 0,
            'fuel': 0
        }
    
    def disconnect(self):
        """Chiude connessione."""
        if self.connection:
            self.connection.close()
            print("[OBD2] Disconnesso")
