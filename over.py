import tkinter as tk
import pyttsx3
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
from langdetect import detect  
from tkinter import filedialog
from gtts import gTTS


engine = pyttsx3.init()

def open_pdf():
    global pdf_reader
    pdf_file = filedialog.askopenfilename(filetypes=[("PDF Documents", "*.pdf"),('Jpg Files', '*.jpg')])
    pdf_reader = PdfReader(pdf_file)
    display_page(0)

def display_page(page_num):
    global text_area
    text_area.delete("1.0", tk.END)
    page = pdf_reader.pages[page_num]
    try:
        text = page.extract_text()  
    except:
        try:
            text = extract_text(pdf_file, page_num=page_num, laparams=LAParams())  
        except Exception as e:
            text = "Error extracting text: {}".format(e)
    text_area.insert(tk.END, text)


def detect_and_convert_to_speech(pdf_path):
    extracted_text = extract_text_from_pdf(pdf_path)
    
    try:
        detected_language = detect(extracted_text)
        
        # Language mapping for gTTS.
        if detected_language == 'en':
            language_code = 'en'
        elif detected_language == 'es':
            language_code = 'es'
        elif detected_language == 'te':  # Add Telugu language code
            language_code = 'te'
        else:
            messagebox.showwarning("Language Not Supported", "Sorry, the detected language is not supported for conversion.")
            return
        
        tts = gTTS(text=extracted_text, lang=language_code, slow=False)
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        os.system(f"start {audio_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")






def speak_selected_text():
    selected_text = text_area.selection_get()
    if selected_text:
        try:
            language = detect(selected_text)  
            voices=engine.getProperty('voices')
            tts=gTTS(text=selected_text,lang='te',slow=False)
            engine.setProperty('voice',voices[1].id)
            engine.setProperty('voice',language)  
        except Exception as e:
            print("Language detection or voice setting failed:", e)
        try:
            engine.say(selected_text)
            engine.runAndWait()
        except Exception as e:
            print("Text-to-speech failed:", e)

root = tk.Tk()

text_area = tk.Text(root)
text_area.pack()

open_button = tk.Button(root, text="Open PDF", command=open_pdf)
open_button.pack()

speak_button = tk.Button(root, text="Speak Selected Text", command=speak_selected_text)
speak_button.pack()

root.mainloop()






