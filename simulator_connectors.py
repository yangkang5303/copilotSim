import xpc
import math

class XPlaneConnector:
    def __init__(self):
        self.client = None
        self.connect()

    def connect(self):
        try:
            self.client = xpc.XPlaneConnect()
        except Exception as e:
            print(f"Failed to connect to X-Plane: {e}")

    def is_connected(self):
        if not self.client:
            return False
        try:
            # Try to read a simple value to verify connection
            self.client.getDREF("sim/test/test_float")
            return True
        except:
            return False

    def get_telemetry(self):
        if not self.client:
            return None
        
        try:
            # DataRefs to read
            # Latitude, Longitude, Altitude (MSL in meters)
            posi = self.client.getPOSI()
            lat = posi[0]
            lon = posi[1]
            alt_meters = posi[2]
            pitch = posi[3]
            roll = posi[4]
            true_heading = posi[5]
            
            # Read indicated airspeed (knots)
            kias = self.client.getDREF("sim/flightmodel/position/indicated_airspeed")[0]
            
            # Read aircraft type (string)
            try:
                # acf_tailnum is often a byte array, let's just get a basic string
                acf_desc = self.client.getDREF("sim/aircraft/view/acf_descrip")[0]
                # Note: getDREF for byte arrays returns floats representing chars, might need decode
                # For simplicity, we will just pass a generic or decoded value if possible
            except:
                acf_desc = "Unknown Aircraft"
                
            # Read ground speed (meters/second to knots)
            gs_ms = self.client.getDREF("sim/flightmodel/position/groundspeed")[0]
            gs_knots = gs_ms * 1.94384
            
            # Altitude in feet
            alt_feet = alt_meters * 3.28084
            
            return {
                "latitude": round(lat, 4),
                "longitude": round(lon, 4),
                "altitude_ft": round(alt_feet),
                "heading": round(true_heading),
                "pitch": round(pitch, 1),
                "roll": round(roll, 1),
                "airspeed_kias": round(kias),
                "groundspeed_kts": round(gs_knots),
                # "aircraft": acf_desc
            }
        except Exception as e:
            print(f"Error reading telemetry: {e}")
            return None

    def close(self):
        if self.client:
            self.client.close()
