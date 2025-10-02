import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Função para garantir que o arquivo não sobrescreva outro
def gerar_nome_unico(diretorio, nome_arquivo):
    contador = 1
    novo_nome = nome_arquivo
    while os.path.exists(os.path.join(diretorio, novo_nome)):
        nome, extensao = os.path.splitext(nome_arquivo)
        novo_nome = f"{nome}-{contador}{extensao}"
        contador += 1
    return novo_nome

# Esta é a classe que vai lidar com os eventos
class MeuMonitor(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"✔️  Arquivo criado: {event.src_path}")
            self.renomear_e_mover_arquivo(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"❌ Arquivo deletado: {event.src_path}")

    def renomear_e_mover_arquivo(self, caminho_arquivo):
        # Obtemos a data atual do sistema
        data_atual = datetime.now().strftime("%Y-%m-%d")  # Formato: ano-mês-dia
        nome, _ = os.path.splitext(caminho_arquivo)  # Ignoramos a extensão original
        novo_nome = f"{os.path.basename(nome)}-{data_atual}.txt"  # Sempre com .txt

        # Obtém o diretório onde o arquivo foi criado
        diretorio_origem = os.path.dirname(caminho_arquivo)

        # Caminho para o diretório de destino (Linux: /tmp)
        novo_diretorio = os.path.join(diretorio_origem, 'renomeados')

        # Cria o diretório 'renomeados' caso não exista
        if not os.path.exists(novo_diretorio):
            os.makedirs(novo_diretorio)

        # Verifica se o arquivo já existe no diretório de destino
        novo_caminho = os.path.join(novo_diretorio, novo_nome)
        
        # Se o arquivo já existe, gera um novo nome único
        if os.path.exists(novo_caminho):
            novo_nome = gerar_nome_unico(novo_diretorio, novo_nome)
            novo_caminho = os.path.join(novo_diretorio, novo_nome)

        # Renomeia e move o arquivo
        try:
            os.rename(caminho_arquivo, novo_caminho)
            print(f"✏️  Arquivo renomeado e movido para: {novo_caminho}")
        except Exception as e:
            print(f"Erro ao renomear ou mover o arquivo {caminho_arquivo}: {e}")


if __name__ == "__main__":
    # Caminho da pasta que será monitorada (Linux)
    caminho_da_pasta = "/caminho/para/a/pasta"  # Altere para o caminho correto
    
    # Verifica se o diretório existe antes de iniciar o monitoramento
    if not os.path.exists(caminho_da_pasta):
        print(f"❌ O caminho {caminho_da_pasta} não existe.")
        exit(1)
    
    # Cria a instância do nosso monitor
    manipulador_de_eventos = MeuMonitor()
    
    # Cria o observador
    observador = Observer()
    
    # Agenda o observador para monitorar a pasta com o nosso manipulador
    observador.schedule(manipulador_de_eventos, caminho_da_pasta, recursive=True)
    
    # Inicia o observador em uma thread separada
    observador.start()
    
    print(f"🚀 Monitorando a pasta '{caminho_da_pasta}'...")
    print("Pressione CTRL+C para parar o monitoramento.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observador.stop()
        print("\n⏹️  Monitoramento parado.")
    
    observador.join()
