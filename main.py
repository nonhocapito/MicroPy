import cv2
import csv
import requests
import numpy as np
from screeninfo import get_monitors
from features import *
import calibration
import os
import time
import json

def get_ip():
    ip=input("Inserire URL IP: http://")
    url=f"http://{ip}/video"
    return url

#legge lo status di un url e restituisce 'True' se paria 200 (tutto ok), 'False' in tutti gli altri casi
def get_status(url):
    try:
        connessione = requests.head(url, timeout=1)
        if connessione.status_code==200:
            return True
    except:
        return False
        
def make_session(name):
    if name=="":
        name=f"unknown"
    
    if os.path.isdir(name)==False:
        os.mkdir(name)
    return name
    
def get_frame(url):
    capture=cv2.VideoCapture(url) #stabilisci connessione
    width=capture.get(cv2.CAP_PROP_FRAME_WIDTH) #larghezza
    height=capture.get(cv2.CAP_PROP_FRAME_HEIGHT) #altezza
    return capture, width, height

def open_window(scale, title):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    
    #leggo risoluzione monitor
    for m in get_monitors():
        x=m.width
        y=m.height
    cv2.resizeWindow(title, int(scale*x), int(scale*y)) # Invertito per rotazione verticale

#legge ip da un file csv e quando ne trova uno valido, lo usa per connettersi
def find_ip(csv_file):
    file=open(csv_file, mode='r', encoding='utf-8')
    reader = list(csv.reader(file))
    for row in reader[1:]:
        ip=row[1]
        test_url=f"{ip}/video"
        if get_status(test_url)==True:
            url=test_url
            print(f"Connetto a {row[0]}")
            break
        else:
            url=""
    return url

#scrive un nuovo ip sul file csv se se ne inserisce uno nuovo valido
def write_csv(csv_file, data):
    with open(csv_file, "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)
        file.close()
#======================================================================================================
#======================================================================================================
def main():
    
    #ottieni indirizzo IP    
    #cerca un IP valido negli utenti salvati
    url=find_ip(users_file)
    
    #se non trova un IP valido, ne chiede uno nuovo.
    if url=="":
        while url=="":
            ip=input("Nessun IP trovato. Inserire nuovo IP: http://")
            test_url=f"http://{ip}/video"
            print(test_url, get_status(test_url))
            
            #se il nuovo IP è valido, lo salva nella lista degli utenti
            if get_status(test_url)==True:
                url=test_url
                ip_name=input("Nuovo IP valido. Inserire nome per salvare: ")
                write_csv(users_file, [ip_name, f"http://{ip}"])
            else:
                url=""

    #connetti
    cap, frame_width, frame_height=get_frame(url)
    print(open("commands.txt", "r").read()) #stampa elenco comandi a schermo
    
    #crea sessione dedicata
    #session_name="test" #DEBUG
    session_name=input("Inserire nome sessione: ")
    session_name=make_session(session_name)
    #cwd=os.getcwd()
    
    s_roi=int((frame_width-frame_height)/2) #calcola dimensione roi (regione di interesse)
    frame_width=int(frame_width)
    frame_height=int(frame_height)
    rot_status={0:"0°", 1:"90° orari", 2:"180°", 3:"270°"} #stati di rotazione
    obj = {"1": "4x", "2": "10x", "3": "40x", "4": "100x"} #obiettivo:ingrandimento
    
    print(f"Dimensioni frame: {frame_width}x{frame_height} px.")
    
    #visualizza frame in una finestra
    scale=0.6 #fattore di scala
    win_name=f"MicroPy Live - {session_name}"
    open_window(scale, win_name)
    wide=True #inizialmente non mostra ROI
    grid=False #inizialmente non mostra griglia
    nod=6 #numero divisioni griglia
    rotation_state = 0 #0=nessuna rotazione, 1=90°orari, 2=180°, 3=90°antiorari
    config = calibration.load_config() #carica calibrazione esistente da file JSON (se esiste)
    id_obj = "1" # Default 4x

    # Dizionario di stato aggiornato
    state = {
        'rif_attuale': config[id_obj]['rif_calib'],
        'px_mm_corrente': config[id_obj]['px_per_mm'], # Fondamentale per la misura!
        'nuovo_px_mm': 0,
        'calib_completata': False,
        'misura_pronta': False,
        'misura_valore': 0,
        'misura_punti': []
    }

    # Associa la callback
    cv2.setMouseCallback(win_name,  #finestra di riferimento
    calibration.mouse_callback,     #richiamo funzione da 'calibration.py'
                        state)      #dizionario

    while True:
    
        #DA ADESSO IN POI AVVIENE TUTTO IN TEMPO REALE, QUINDI A QUESTO LIVELLO DI ANNIDAMENTO
        ret, frame = cap.read()
        key = cv2.waitKey(1) & 0xFF #attesa aggiornamento (1 millisecondo)
        
        # Modifica il dizionario 'state' se l'utente cambia obiettivo (tasti 1-4)
        # Nel loop while del main.py

        if key in [ord('1'), ord('2'), ord('3'), ord('4')]:
            id_obj = chr(key)
            # 1. Recupera il valore corretto dal JSON per il NUOVO obiettivo
            nuovo_rapporto = config[id_obj]['px_per_mm']
            # 2. AGGIORNA IL DIZIONARIO che legge il mouse (state o param)
            # Senza questa riga, il mouse userà sempre il valore iniziale!
            state['px_mm_corrente'] = nuovo_rapporto
            # 3. Aggiorna anche il riferimento per la calibrazione
            state['rif_attuale'] = config[id_obj]['rif_calib']
            print(f"Cambio obiettivo: {config[id_obj]['label']} - Rapporto: {nuovo_rapporto:.3f} px/mm")
        
        if key==ord("q"):   #chiude il programma premendo Q
            print("Chiusura")
            break
        
        # Se premi 'g', mostra/nascondi griglia
        if key == ord('g'):
            grid = not grid  # inverte il booleano per la griglia
            dx, dy=get_grid_dim(frame, nod)
            print(f"Griglia {f'ON (div x = {dx} px, div y={dy} px)' if grid else 'OFF'}")
        
        #attiva/disattiva regione di interesse
        if key==ord("w"):
            wide = not wide # inverte il booleano per il wide
            print(f"Regione di interesse {'OFF' if wide else f'ON ({frame_width-2*s_roi}x{frame_width-2*s_roi} px)'}")
        
        #rotazione se premo R
        if key==ord("r"):
            rotation_state = (rotation_state + 1) % 4 #assegna nuova rotazione
            print(f"Rotazione {rot_status[rotation_state]}")
        
        #calibrazione se premo K
        if key==ord("k"):
            calibration.calibrating = True  #cambia lo stato di calibrating in 'calibration.py'
            print(f"\n >MODALITÀ CALIBRAZIONE:\n\t-Usa un riferimento di {state['rif_attuale']} mm sul vetrino.")
        
        #se il mouse ha finito la calibrazione, salva nel JSON
        if state['calib_completata']:
            config[id_obj]['px_per_mm'] = state['nuovo_px_mm']
            calibration.save_config(config)
            state['calib_completata'] = False
        
        # Tasto per misurare
        if key == ord('m'):
            calibration.measuring = True
            state['misura_pronta'] = False # Resetta la misura precedente
            print("\n >MODALITÀ MISURAZIONE:\n\t-Clicca due punti sul video")
        
        # Applica/nasconde cambiamenti
        frame = show_grid(frame, grid, nod) #GRIGLIA (nod=numero di divisioni)
        frame=region_of_interest(frame, wide, s_roi) #ROI (region of interest)
        frame=rotate_frame(frame, rotation_state) #ROTAZIONE
        
        # Disegno della misura (prima di imshow)
        if state['misura_pronta']:
            draw_measurement(frame, state['misura_punti'], state['misura_valore'])
        
        # Tasto per CANCELLARE la misura
        if key == ord('c'):
            state['misura_pronta'] = False
            state['misura_punti'] = []
            state['misura_valore'] = 0
            print("\t-Misura cancellata.")
        
        # Disegna la barra passando il px_per_mm e il riferimento dal JSON
        frame = draw_scale_bar(
            frame, 
            config[id_obj]['px_per_mm'], 
            config[id_obj]['label'], 
            session_name,
            config[id_obj]['rif_calib']
        )
        
        # Mostra il frame nella finestra
        cv2.imshow(win_name, frame) #mostra frame
        
        #salva frame come immagine (mantenendo tutte le modifiche)
        if key==ord("s"):
            timestamp = time.strftime("%d-%m-%Y_%H%M%S")
            path=os.path.join(cwd, session_name)
            cv2.imwrite(f"{path}/{session_name}_{timestamp}.png", frame)
            print("Immagine acquisita.")
            
#======================================================================================================
#======================================================================================================

cwd=os.getcwd()
users_file="users.csv"

#se users_file non esiste lo crea
if os.path.isfile( os.path.join(cwd, users_file) )==False:
    write_csv( os.path.join(cwd, users_file), ["user","ip"])
    write_csv( os.path.join(cwd, users_file), ["",""])
if __name__ == "__main__":
    main()
