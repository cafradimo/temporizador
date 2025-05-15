import time
import pygame
from gtts import gTTS
import os
import tempfile

def inicializar_pygame():
    """Inicializa o mixer do pygame uma única vez"""
    try:
        pygame.mixer.init()
    except Exception as e:
        print(f"Erro ao inicializar o mixer de áudio: {e}")
        return False
    return True

def falar(texto, lingua='pt-br'):
    """Converte texto em fala usando gTTS e reproduz"""
    try:
        # Cria um arquivo temporário
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as fp:
            temp_path = fp.name
        
        # Gera o áudio e salva no arquivo temporário
        tts = gTTS(text=texto, lang=lingua, slow=False)
        tts.save(temp_path)
        
        # Reproduz o áudio
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        # Espera a mensagem de voz terminar
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        # Remove o arquivo temporário após uso
        try:
            os.unlink(temp_path)
        except:
            pass
            
    except Exception as e:
        print(f"Erro ao reproduzir mensagem de voz: {e}")
        try:
            os.unlink(temp_path)
        except:
            pass

def tocar_musica(arquivo_musica):
    """Reproduz um arquivo de música"""
    try:
        if not os.path.exists(arquivo_musica):
            print(f"Arquivo de música não encontrado: {arquivo_musica}")
            return False
            
        pygame.mixer.music.load(arquivo_musica)
        pygame.mixer.music.play()
        return True
        
    except Exception as e:
        print(f"Erro ao reproduzir música: {e}")
        return False

def temporizador(segundos):
    """Contagem regressiva com anúncio de voz ao final"""
    print(f"Temporizador iniciado por {segundos} segundos...")
    
    # Contagem regressiva
    for i in range(segundos, 0, -1):
        print(f"Tempo restante: {i} segundos")
        time.sleep(1)
    
    # Mensagem de voz ao finalizar
    mensagem = f"Esta mensagem se auto destruirá em {segundos} segundos"
    falar(mensagem)
    
    # Tocar tema de Missão Impossível
    print("Reproduzindo tema de Missão Impossível...")
    
    # Verifica se o arquivo existe
    arquivo_musica = "missao_impossivel.mp3"
    if not os.path.exists(arquivo_musica):
        print("""
        Arquivo de música não encontrado!
        Por favor, baixe o tema de Missão Impossível em MP3 e:
        1. Salve como 'missao_impossivel.mp3' no mesmo diretório do script
        2. Ou modifique a variável 'arquivo_musica' no código
        """)
    else:
        tocar_musica(arquivo_musica)

def main():
    # Inicializa o pygame uma vez no início
    if not inicializar_pygame():
        print("Não foi possível inicializar o sistema de áudio")
        return
    
    try:
        segundos = int(input("Digite o tempo em segundos para o temporizador: "))
        if segundos <= 0:
            print("Por favor, digite um número positivo maior que zero.")
            return
            
        temporizador(segundos)
        
        # Mantém o programa rodando enquanto a música está tocando
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
    except ValueError:
        print("Por favor, digite um número válido.")
    except KeyboardInterrupt:
        print("\nTemporizador cancelado pelo usuário.")
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    # Verifica e instala dependências necessárias
    try:
        import pygame
        from gtts import gTTS
    except ImportError:
        print("Instalando dependências necessárias...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame", "gTTS"])
        
    main()