import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wav
from scipy.fft import fft
from pydub import AudioSegment
import subprocess


def load_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.mp4")])
    if file_path:
        button.config(text=file_path.split('/')[-1])
        process_audio(file_path)


def calculate_rt60(data, sample_rate):
    # Energy decay curve
    energy = data ** 2
    cumulative_energy = np.cumsum(energy[::-1])[::-1]
    cumulative_energy = cumulative_energy / cumulative_energy[0]  # Normalize
    # RT60 estimation
    rt60_time = np.where(cumulative_energy < 0.001)[0]
    if len(rt60_time) > 0:
        rt60 = rt60_time[0] / sample_rate
    else:
        # No clear RT60 found
        rt60 = -1
    return rt60


def process_audio(file_path):
    correct_file = ""
    # Check if the audio file is .wav and converts it into a valid file if it isn't
    if (file_path[(len(file_path) - 3):(len(file_path))] != "wav"):
        subprocess.run(["powershell", "ffmpeg -i " + file_path + " " + file_path.replace(
            file_path[(len(file_path) - 3):(len(file_path))], "wav")], shell=True)
        correct_file = file_path.replace(file_path[(len(file_path) - 3):(len(file_path))], "wav")
    else:
        correct_file = file_path

    print(correct_file)
    sample_rate, data = wav.read(correct_file)

    # If audio is stereo, convert to mono
    if len(data.shape) > 1 and data.shape[1] == 2:
        data = data.mean(axis=1)

    # Time array
    time = np.arange(0, len(data)) / sample_rate

    # Compute FFT
    fft_data = fft(data)
    freqs = np.fft.fftfreq(len(fft_data), 1 / sample_rate)
    magnitude = np.abs(fft_data)

    # Find frequency of greatest amplitude
    max_amp_idx = np.argmax(magnitude)
    freq_of_max_amp = freqs[max_amp_idx]

    # Calculate RT60
    combined_rt60 = calculate_rt60(data, sample_rate)

    # Separate frequencies into Low, Mid, and High
    low_freq = data[freqs < 300]
    mid_freq = data[(freqs >= 300) & (freqs < 3000)]
    high_freq = data[freqs >= 3000]

    # RT60 for frequency bands
    low_rt60 = calculate_rt60(low_freq, sample_rate)
    mid_rt60 = calculate_rt60(mid_freq, sample_rate)
    high_rt60 = calculate_rt60(high_freq, sample_rate)

    # Plot waveforms and magnitude spectra
    fig, axes = plt.subplots(3, 3, figsize=(15, 10))
    axes[0, 0].plot(time[:len(low_freq)], low_freq, color='blue')
    axes[0, 0].set_title('Low Frequency Waveform')
    axes[0, 1].magnitude_spectrum(low_freq, Fs=sample_rate, scale='dB', color='blue')
    axes[0, 2].plot(time[:len(low_freq)], np.cumsum(low_freq[::-1])[::-1], color='blue')
    axes[0, 2].set_title('Low Frequency RT60 Decay')

    axes[1, 0].plot(time[:len(mid_freq)], mid_freq, color='green')
    axes[1, 0].set_title('Mid Frequency Waveform')
    axes[1, 1].magnitude_spectrum(mid_freq, Fs=sample_rate, scale='dB', color='green')
    axes[1, 2].plot(time[:len(mid_freq)], np.cumsum(mid_freq[::-1])[::-1], color='green')
    axes[1, 2].set_title('Mid Frequency RT60 Decay')

    axes[2, 0].plot(time[:len(high_freq)], high_freq, color='red')
    axes[2, 0].set_title('High Frequency Waveform')
    axes[2, 1].magnitude_spectrum(high_freq, Fs=sample_rate, scale='dB', color='red')
    axes[2, 2].plot(time[:len(high_freq)], np.cumsum(high_freq[::-1])[::-1], color='red')
    axes[2, 2].set_title('High Frequency RT60 Decay')

    plt.tight_layout()
    plt.show()

    # Combined RT60 plot
    plt.figure(figsize=(8, 6))
    bands = ['Low', 'Mid', 'High']
    rt60_values = [low_rt60, mid_rt60, high_rt60]
    plt.bar(bands, rt60_values, color=['blue', 'green', 'red'])
    plt.title('RT60 for Frequency Bands')
    plt.ylabel('RT60 (seconds)')
    plt.show()

    # RT60 differences
    baseline = 0.5
    low_diff = low_rt60 - baseline
    mid_diff = mid_rt60 - baseline
    high_diff = high_rt60 - baseline
    combined_diff = combined_rt60 - baseline

    # Output text information
    print(f"Time Duration: {time[-1]:.2f} seconds")
    print(f"Frequency of Greatest Amplitude: {freq_of_max_amp:.2f} Hz")
    print(f"Combined RT60: {combined_rt60:.2f} seconds (Difference from 0.5s: {combined_diff:+.2f} seconds)")
    print(f"Low Frequency RT60: {low_rt60:.2f} seconds (Difference from 0.5s: {low_diff:+.2f} seconds)")
    print(f"Mid Frequency RT60: {mid_rt60:.2f} seconds (Difference from 0.5s: {mid_diff:+.2f} seconds)")
    print(f"High Frequency RT60: {high_rt60:.2f} seconds (Difference from 0.5s: {high_diff:+.2f} seconds)")


# GUI setup
root = tk.Tk()
root.title("Python Interactive Data Acoustic Modeling")

root.geometry("500x300")

button = tk.Button(root, text="Open a File", command=load_audio_file)
button.pack(pady=100)

root.mainloop()