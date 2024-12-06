import tkinter as tk
from tkinter import filedialog

def load_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.ogg *.flac")])
    if file_path:
        button.config(text=file_path.split('/')[-1])

root = tk.Tk()
root.title("Python Interactive Data Acoustic Modeling")

root.geometry("500x300")

button = tk.Button(root, text="Open a File", command=load_audio_file)
button.pack(pady=100)

root.mainloop()