import numpy as np
import wave
import sounddevice as sd
global names
names=""
def text_to_binary(text):
    """Converte o texto em uma string binária."""
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string

def file_to_binary(file_path):
    """Lê um arquivo binário e converte para uma string binária."""
    with open(file_path, 'rb') as f:
        binary_data = f.read()
    binary_string = ''.join(format(byte, '08b') for byte in binary_data)
    return binary_string

def combine_text_and_file(texts, file_path):
    """Combina o texto binário com os dados binários do arquivo."""
    file_binary = file_to_binary(file_path)
    ff=""
    for a in range(127):
         ff=ff+str(chr(85))
    bn=len(file_binary)/8
    ii=int(bn//256)
    iii=int(bn-(ii*256))
    ff=ff+str(chr(0))+str(chr(0))+names+str(chr(iii))+str(chr(ii))+str(chr(0))+str(chr(0))+str(chr(0))
    text=ff
    text_binary = text_to_binary(text)
    
    combined_binary = text_binary + file_binary
    return combined_binary

def generate_zx_spectrum_audio(binary_data, sample_rate=44100):
    """Gera um sinal de áudio que representa os dados binários no formato ZX Spectrum."""
    pulse_0_length = int(sample_rate / 1000)  # Duração do pulso para '0' em samples
    pulse_1_length = int(sample_rate / 500)   # Duração do pulso para '1' em samples

    audio_data = []
    for bit in binary_data:
        if bit == '0':
            pulse = np.ones(pulse_0_length)
        else:
            pulse = np.ones(pulse_1_length)
        audio_data.extend(pulse)
        audio_data.extend(np.zeros(pulse_0_length))  # Pequena pausa entre pulsos

    audio_data = np.array(audio_data, dtype=np.float32) * 0.5  # Normaliza o volume
    return audio_data

def save_wave_file(filename, audio_data, sample_rate):
    """Salva os dados de áudio em um arquivo WAV."""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())

def main():
    global names
    # Solicita o nome do arquivo binário ao usuário
    print("\x1bc\x1b[47;34m")
    file_path = input("Digite o nome do arquivo binário: ")
    names=file_path+"            "
    names=names[:10]
   

    # Combina o texto com o arquivo binário
    combined_binary = combine_text_and_file(names, file_path)

    # Gera o áudio no formato ZX Spectrum
    audio_data = generate_zx_spectrum_audio(combined_binary)

    # Toca o áudio
    sd.play(audio_data, samplerate=44100)
    sd.wait()

    # Salva o áudio em um arquivo WAV
    output_filename = "output.wav"
    save_wave_file(output_filename, audio_data, sample_rate=44100)

    print(f"Áudio salvo em {output_filename}")

if __name__ == "__main__":
    main()



