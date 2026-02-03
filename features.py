import cv2

#disegna una griglia sul frame con tante maglie quante indicate da 'nod' (numero di divisioni)
def show_grid(frame, status, nod):
    if status==True: #status true=visualizza griglia
        height, width = frame.shape[:2] # altezza e larghezza del frame
        x_step=int(width/nod) #passo linee verticali
        y_step=int(height/nod) #passo linee orizzontali

        # righe verticali
        for x in range(0, width, x_step):
            # cv2.line(immagine, punto_inizio, punto_fine, colore, spessore)
            cv2.line(frame, (x, 0), (x, width), (255, 255, 255), 1)
        
        #righe orizzontali
        for y in range(0, height, y_step):
            # cv2.line(immagine, punto_inizio, punto_fine, colore, spessore)
            cv2.line(frame, (0, y), (width, y), (255, 255, 255), 1)

        return frame#, x_step, y_step
    else:
        return frame

def get_grid_dim(frame, nod):
    height, width=frame.shape[:2]
    dx=width/nod
    dy=height/nod
    return dx, dy

def region_of_interest(frame, status, s_roi):
    height, width=frame.shape[:2]
    if status==False:
        frame=frame[0:height, s_roi: width-s_roi]
        return frame
    else:
        return frame
        
def rotate_frame(frame, rotation_state):
    
    if rotation_state==1:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif rotation_state==2:
        frame = cv2.rotate(frame, cv2.ROTATE_180)
    elif rotation_state==3:
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return frame

def draw_scale_bar(
            frame,      
            px_per_mm,      #quanti pixel in 1 mm
            obj_label,      #identificativo obiettivo corrente
            session_name,   #nome della sessione corrente
            rif_visualizzato):
            
    h, w = frame.shape[:2]
    
    # Fascia nera di fondo
    cv2.rectangle(frame, (0, h - 50), (w, h), (0, 0, 0), -1)

    # Calcola lunghezza barra (deve essere INT per cv2.line)
    # Se px_per_mm è 10000 e rif_visualizzato è 0.01, la barra sarà lunga 100px
    bar_length = int(px_per_mm * rif_visualizzato)
    
    # Coordinate barra
    margin_right = 30
    bar_y = h - 15
    start_pt = (w - margin_right - bar_length, bar_y)
    end_pt = (w - margin_right, bar_y)
    
    # Disegna linea bianca
    cv2.line(frame, start_pt, end_pt, (255, 255, 255), 2)

    # Testo sopra la barra
    # Convertiamo 0.01 mm in "10 um" per leggibilità se necessario
    label_barra = f"{rif_visualizzato} mm"
    
    if rif_visualizzato < 0.1:
        label_barra = f"{int(rif_visualizzato * 1000)} um"

    cv2.putText(frame, label_barra, (start_pt[0], bar_y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Label Obiettivo e Sessione
    info_text = f"{session_name} | {obj_label}"
    cv2.putText(frame,
            info_text,  #testo
            (20, h - 18), #coordinate posizione
            cv2.FONT_HERSHEY_SIMPLEX, #font
            0.5, #dimensione carattere
            (0, 255, 255), #colore
            1, #spessore carattere
            cv2.LINE_AA) #stile carattere
            
    return frame

def draw_measurement(frame, punti, valore_mm):
    if len(punti) == 2:
        p1, p2 = punti
        
        # Scegliamo l'unità di misura e il testo
        # Se il valore è minore di 0.1 mm, passiamo ai micron
        if valore_mm < 0.1:
            valore_finale = valore_mm * 1000
            unita = "um"
            decimali = 1 # es: 10.5 um
        else:
            valore_finale = valore_mm
            unita = "mm"
            decimali = 3 # es: 0.125 mm

        testo = f"{valore_finale:.{decimali}f} {unita}"

        # DISEGNO GRAFICO
        # Linea verde con Anti-Aliasing
        cv2.line(frame, p1, p2, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Punti di ancoraggio (piccoli cerchi pieni)
        cv2.circle(frame, p1, 5, (0, 255, 0), -1)
        cv2.circle(frame, p2, 5, (0, 255, 0), -1)

        # Posizionamento del testo (un po' più in alto e a destra del secondo punto)
        pos_testo = (int(p2[0] + 15), int(p2[1] - 15))
        
        # (Opzionale) Sfondo nero dietro al testo per renderlo leggibile su ogni immagine
        t_size = cv2.getTextSize(testo, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        cv2.rectangle(frame, 
                      (pos_testo[0] - 5, pos_testo[1] - t_size[1] - 5), 
                      (pos_testo[0] + t_size[0] + 5, pos_testo[1] + 5), 
                      (0, 0, 0), -1)

        cv2.putText(frame, testo, pos_testo, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
