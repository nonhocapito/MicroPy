import cv2
import json
import os
import numpy as np

CALIB_FILE="objectives.json"
punti_calib=[]
punti_misura=[]
calibrating=False
measurment=False

#Carica il database obiettivi o ne crea uno di default
def load_config():
    if os.path.exists(CALIB_FILE):
        with open(CALIB_FILE, 'r') as f:
            return json.load(f)
    
    # Default se il file non esiste
    return {
        "1": {"label": "4x", "px_per_mm": 100.0, "rif_calib": 1.0}, #ingrandimento, pixel per mm, lunghezza di riferimento
        "2": {"label": "10x", "px_per_mm": 250.0, "rif_calib": 1.0},
        "3": {"label": "40x", "px_per_mm": 1000.0, "rif_calib": 0.1},
        "4": {"label": "100x", "px_per_mm": 2500.0, "rif_calib": 0.01}
    }

#funzione di salvataggio json
def save_config(data):
    with open(CALIB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Variabili di stato interne al modulo per gestire i clic
punti_calib = []
punti_misura = []
calibrating = False
measuring = False

def mouse_callback(event, x, y, flags, param):
    """
    Gestisce l'interazione con il mouse.
    param: dizionario 'state' passato dal main che deve contenere:
           - 'rif_attuale': float (es. 1.0 o 0.01)
           - 'px_mm_corrente': float (il valore caricato dal JSON)
    """
    global punti_calib, calibrating, punti_misura, measuring

    if event == cv2.EVENT_LBUTTONDOWN:
        
        # --- CASO 1: CALIBRAZIONE (Tasto 'k') ---
        if calibrating:
            punti_calib.append((x, y))
            print(f"\t-Punto {len(punti_calib)} registrato (x={x}, y={y})")
            
            if len(punti_calib) == 2:
                # Calcola distanza euclidea in pixel
                dist_px = np.sqrt((punti_calib[1][0] - punti_calib[0][0])**2 + 
                                  (punti_calib[1][1] - punti_calib[0][1])**2)
                
                # Usa il riferimento impostato nel main per l'obiettivo attuale
                riferimento = param.get('rif_attuale', 1.0)
                
                # Calcola il nuovo rapporto pixel/mm
                nuovo_px_mm = dist_px / riferimento
                
                # Restituisce i dati al main tramite il dizionario
                param['nuovo_px_mm'] = nuovo_px_mm
                param['calib_completata'] = True
                
                # Reset stato calibrazione
                punti_calib = []
                calibrating = False
                print(f"\t-Calibrazione terminata. Nuovo rapporto: {nuovo_px_mm:.2f} px/mm")

        # --- CASO 2: MISURAZIONE (Tasto 'm') ---
        elif measuring:
            punti_misura.append((x, y))
            print(f"\t-Punto {len(punti_misura)}: (x={x}, y={y})")
            
            if len(punti_misura) == 2:
                # Calcola distanza in pixel
                dist_px = np.sqrt((punti_misura[1][0] - punti_misura[0][0])**2 + 
                                  (punti_misura[1][1] - punti_misura[0][1])**2)
                
                # IMPORTANTE: Prende il valore PX/MM CORRENTE dell'obiettivo attivo
                # Questo valore viene aggiornato dal main quando premi 1, 2, 3 o 4
                rapporto_attuale = param.get('px_mm_corrente', 1.0)
                
                # Calcola la distanza reale in mm
                dist_mm = dist_px / rapporto_attuale
                
                # Restituisce i dati al main per il disegno in features.py
                param['misura_valore'] = dist_mm
                param['misura_punti'] = list(punti_misura)
                param['misura_pronta'] = True
                
                # Reset stato misurazione
                punti_misura = []
                measuring = False
                print(f"\t-Distanza = {dist_mm:.4f} mm")
