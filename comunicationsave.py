
import numpy as np
import sounddevice as sd
#pip install sounddevice
# Frequências usadas pelo ZX Spectrum
FREQ_0 = 1300  # Frequência para o bit 0
FREQ_1 = 2600  # Frequência para o bit 1
SAMPLING_RATE = 44100  # Taxa de amostragem para o áudio

def text_to_zx_audio(text):
    def create_tone(frequency, duration):
        t = np.linspace(0, duration, int(SAMPLING_RATE * duration), endpoint=False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        return wave

    def append_bit(wave, bit):
        if bit == '0':
            return np.concatenate((wave, create_tone(FREQ_0, 1/220.0)))
        else:
            return np.concatenate((wave, create_tone(FREQ_1, 1/220.0)))
    
    # Convert text to binary representation
    binary_data = ''.join(format(ord(char), '08b') for char in text)
    
    # Add pilot tone and sync byte (not fully accurate but for demonstration)
    wave = create_tone(2000,  1.0/220.0*128.0 )  # 1-second pilot tone
    wave = np.concatenate((wave, create_tone(FREQ_0, 1/220.0)))  # Sync byte (just using one '0' bit for simplicity)

    # Encode the binary data into the wave
    for bit in binary_data:
        wave = append_bit(wave, bit)
    
    return wave

def main():
    # Get text input from user
    input_text = input("Enter the text to convert to ZX Spectrum audio: ")
    
    # Convert text to ZX Spectrum audio
    audio_wave = text_to_zx_audio(input_text)
    
    # Play the audio wave
    print("Playing audio...")
    sd.play(audio_wave, SAMPLING_RATE)
    sd.wait()  # Wait until the audio finishes playing
    print("Audio playback finished.")
print("\x1bc\x1b[47;34m")
if __name__ == "__main__":
    main()
