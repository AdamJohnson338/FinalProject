import tkinter as tk
from tkinter import filedialog
import natplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import spectrogram
from scipy.fft import fft

def load_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.ogg *.flac")])
    if file_path:
        button.config(text=file_path.split('/')[-1])
        process_audio(file_path)
        
def process_audio(file_path)
    #Load the audio file
    
    # Time array
    time = np.arange(0, len(data)) / sample_rate

    # Compute FFT
    fft_data = fft(data)
    freqs = np.fft.fftfreq(len(fft_data), 1 / sample_rate)
    magnitude = np.abs(fft_data)
    
    # Find frequency of greatest amplitude
    max_amp_idx = np.argmax(magnitude)
    freq_of_max_amp = freqs[max_amp_idx]
    
    #Calculate RT60
    energy = data ** 2
    cumulativr_energy = np.cumsum(energy[::-1])[::-1]
    rt60 = -np.log10(0.001) / (np.log10(cumulative_energy[0]) - np.log10(cumulative_energy[-1])) / sample_rate
    
    # Separate frequencies into Low, Mid, and High
    low_freq = data[freqs < 300]
    mid_freq = data[(freqs >= 300) & (freqs < 3000)]
    high_freq = data[freqs >= 3000]
    
    # Plot waveforms
    fig, axes = plt.subplots(3, 2, figsize=(12, 8))
    axes[0, 0].plot(time, low_freq, color='blue')
    axes[0, 0].set_title('Low Frequency Waveform')
    axes[0, 1].magnitude_spectrum(low_freq, Fs=sample_rate, scale='dB', color='blue')

    axes[1, 0].plot(time, mid_freq, color='green')
    axes[1, 0].set_title('Mid Frequency Waveform')
    axes[1, 1].magnitude_spectrum(mid_freq, Fs=sample_rate, scale='dB', color='green')

    axes[2, 0].plot(time, high_freq, color='red')
    axes[2, 0].set_title('High Frequency Waveform')
    axes[2, 1].magnitude_spectrum(high_freq, Fs=sample_rate, scale='dB', color='red')
    
    plt.tight_layout()
    plt.show()

    # Output text information
    print(f"Time Duration: {time[-1]:.2f} seconds")
    print(f"Frequency of Greatest Amplitude: {freq_of_max_amp:.2f} Hz")
    print(f"RT60: {rt60:.2f} seconds")
# GUI setup
root = tk.Tk()
root.title("Python Interactive Data Acoustic Modeling")

root.geometry("500x300")

button = tk.Button(root, text="Open a File", command=load_audio_file)
button.pack(pady=100)

root.mainloop()
