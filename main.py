import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
import threading

def transcribe_audio_and_update_ui(audio_file_path: str):
    """Trascrive l'audio e aggiorna l'interfaccia utente."""
    transcription_text.config(state=tk.DISABLED)  # Disabilita la casella di testo
    select_button.config(state=tk.DISABLED)  # Disabilita il pulsante
    copy_button.config(state=tk.DISABLED)  # Disabilita il pulsante di copia
    transcription_text.delete("1.0", tk.END)  # Cancella il testo precedente

    def transcribe_local_audio():
        """Funzione interna per la trascrizione locale dell'audio."""
        recognizer = sr.Recognizer()
        transcript = ""

        with sr.AudioFile(audio_file_path) as audio_file:
            audio_data = recognizer.record(audio_file)

        try:
            transcript = recognizer.recognize_google(audio_data, language="it-IT")
        except sr.UnknownValueError:
            transcript = "Non ho capito bene, potresti ripetere?"
        except sr.RequestError as e:
            transcript = f"Impossibile ottenere i risultati dal servizio di riconoscimento vocale; {e}"

        return transcript

    # Avvia la funzione di trascrizione audio in un thread separato
    thread = threading.Thread(target=transcribe_local_audio)
    thread.start()

    # Funzione di callback per aggiornare l'interfaccia utente dopo la trascrizione
    def update_ui_after_transcription():
        """Aggiorna l'interfaccia utente con il testo trascritto."""
        transcription = transcribe_local_audio()
        transcription_text.config(state=tk.NORMAL)  # Riabilita la casella di testo
        transcription_text.delete("1.0", tk.END)  # Cancella il testo precedente
        transcription_text.insert(tk.END, transcription)
        transcription_text.config(fg="black", font=("Arial", 10))
        select_button.config(state=tk.NORMAL)  # Riabilita il pulsante
        copy_button.config(state=tk.NORMAL)  # Riabilita il pulsante di copia

    # Avvia una funzione di callback dopo che la trascrizione è completata
    root.after(100, update_ui_after_transcription)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.flac;")])
    if file_path:
        transcribe_audio_and_update_ui(file_path)

def copy_transcription():
    """Copia il testo trascritto negli appunti."""
    root.clipboard_clear()
    root.clipboard_append(transcription_text.get("1.0", tk.END))

# Creazione della finestra principale
root = tk.Tk()
root.title("El Sbobinator")

# Frame per il pulsante e il campo di testo
frame = tk.Frame(root)
frame.pack(pady=20)

# Pulsante per selezionare il file audio
select_button = tk.Button(frame, text="Seleziona File", command=select_file, bg="orange", fg="white", font=("Arial", 12, "bold"))
select_button.pack(side=tk.TOP, padx=10, pady=5)

# Pulsante per copiare il testo trascritto
copy_button = tk.Button(frame, text="Copia Testo", command=copy_transcription, bg="blue", fg="white", font=("Arial", 12, "bold"), state=tk.DISABLED)
copy_button.pack(side=tk.TOP, padx=10, pady=5)

# Campo di testo per la trascrizione
transcription_text = tk.Text(frame, height=10, width=50, bg="lightgray", fg="black", font=("Arial", 10))
transcription_text.pack(side=tk.TOP, padx=10, pady=5)

# Esecuzione della finestra principale
root.mainloop()
