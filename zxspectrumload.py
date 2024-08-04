import numpy as np
import wave

def read_wave_file(filename):
    """Lê os dados de áudio de um arquivo WAV."""
    with wave.open(filename, 'rb') as wf:
        sample_rate = wf.getframerate()
        num_frames = wf.getnframes()
        audio_data = wf.readframes(num_frames)
        audio_data = np.frombuffer(audio_data, dtype=np.int16)
    return audio_data, sample_rate

def decode_zx_spectrum_audio(audio_data, sample_rate):
    """Decodifica o áudio ZX Spectrum em dados binários."""
    pulse_0_length = int(sample_rate / 1000)  # Duração do pulso para '0' em samples
    pulse_1_length = int(sample_rate / 500)   # Duração do pulso para '1' em samples

    threshold = 0.25 * 32767  # Um valor de threshold arbitrário para distinguir pulsos
    bitstream = []
    
    i = 0
    while i < len(audio_data):
        if audio_data[i] > threshold:
            # Contar a duração do pulso
            pulse_length = 1
            while i + pulse_length < len(audio_data) and audio_data[i + pulse_length] > threshold:
                pulse_length += 1

            if pulse_length >= pulse_1_length:
                bitstream.append('1')
            else:
                bitstream.append('0')
            
            # Pular a duração do pulso e a pausa entre pulsos
            i += pulse_length + pulse_0_length
        else:
            i += 1
    
    return ''.join(bitstream)

def binary_to_text(binary_data):
    """Converte dados binários em texto."""
    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def binary_to_file(binary_data, output_filename):
    """Converte dados binários em um arquivo binário."""
    byte_array = bytearray()
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            byte_array.append(int(byte, 2))
    with open(output_filename, 'wb') as f:
        f.write(byte_array)

def main():
    # Solicita o nome do arquivo WAV ao usuário
    filename = input("Digite o nome do arquivo WAV: ")

    # Lê o arquivo WAV
    audio_data, sample_rate = read_wave_file(filename)
    
    # Decodifica o áudio para dados binários
    binary_data = decode_zx_spectrum_audio(audio_data, sample_rate)
    
    # Separa o texto dos dados binários
    text_length = 128  # Exemplo: ajusta de acordo com o seu caso
    xxxx= binary_data[:128*8]
    text_length=(binary_to_text(xxxx)).find('\0')+1
    text_binary = binary_data[:text_length*8+16*8]
    file_binary = binary_data[text_length*8+16*8:]
    
    # Converte o texto binário de volta para texto
    text = binary_to_text(text_binary)
    
    # Converte os dados binários para um arquivo binário
    output_filename = "output.bin"
    binary_to_file(file_binary, output_filename)
    
    # Exibe o texto e salva o arquivo binário
    print("Texto decodificado:")
    print(text)
    print(f"Arquivo binário salvo em {output_filename}")
print("\x1bc\x1b[47;34m")
if __name__ == "__main__":
    main()
