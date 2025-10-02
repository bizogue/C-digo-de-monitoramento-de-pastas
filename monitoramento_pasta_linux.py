import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# --- Configurações/Constantes ---
# Define o formato de data que será anexado aos nomes dos arquivos
DATA_FORMATO = "%Y-%m-%d" 
# Define o nome da subpasta de destino onde os arquivos serão movidos
SUBPASTA_DESTINO = 'renomeados'
# Define a extensão padrão de saída (o código atual força para .txt, se a intenção for preservar, esta linha pode ser removida)
EXTENSAO_SAIDA = '.txt'


def gerar_nome_unico(diretorio, nome_arquivo):
    """
    Gera um nome de arquivo único adicionando um contador (-1, -2, etc.)
    ao nome base se o arquivo de destino já existir.

    Args:
        diretorio (str): O caminho completo para o diretório de destino.
        nome_arquivo (str): O nome base do arquivo, com sua extensão.

    Returns:
        str: O nome de arquivo único garantido.
    """
    contador = 1
    novo_nome = nome_arquivo
    
    # Verifica se o arquivo já existe no destino. Se sim, entra no loop.
    while os.path.exists(os.path.join(diretorio, novo_nome)):
        # Separa o nome do arquivo da sua extensão.
        nome, extensao = os.path.splitext(nome_arquivo)
        
        # Cria um novo nome, anexando o contador.
        # Exemplo: 'doc-2025-10-02.txt' -> 'doc-2025-10-02-1.txt'
        novo_nome = f"{nome}-{contador}{extensao}"
        contador += 1
        
    return novo_nome


class MeuMonitor(FileSystemEventHandler):
    """
    Manipulador de Eventos (Handler) customizado para o watchdog.
    Define as ações a serem tomadas quando eventos do sistema de arquivos ocorrem.
    """
    def on_created(self, event):
        """
        Executado quando um novo arquivo ou diretório é criado.
        Aplica a lógica de renomeação e movimentação apenas para arquivos.
        """
        if not event.is_directory:
            print(f"✔️  Arquivo criado: {event.src_path}")
            self.renomear_e_mover_arquivo(event.src_path)

    def on_deleted(self, event):
        """
        Executado quando um arquivo ou diretório é deletado.
        Apenas loga a ação para fins de monitoramento.
        """
        if not event.is_directory:
            print(f"❌ Arquivo deletado: {event.src_path}")

    def renomear_e_mover_arquivo(self, caminho_arquivo):
        """
        Renomeia o arquivo com a data atual e o move para um subdiretório
        de destino (definido por SUBPASTA_DESTINO).

        Args:
            caminho_arquivo (str): O caminho completo do arquivo recém-criado.
        """
        # --- 1. Geração do Novo Nome ---
        data_atual = datetime.now().strftime(DATA_FORMATO)
        
        # Extrai apenas o nome do arquivo, ignorando o diretório e a extensão original
        nome_base_sem_ext = os.path.splitext(os.path.basename(caminho_arquivo))[0]
        
        # Cria o nome padrão de destino: [NomeOriginal]-[Data].txt
        # NOTA: O código força a extensão para .txt, ignorando a original.
        nome_destino = f"{nome_base_sem_ext}-{data_atual}{EXTENSAO_SAIDA}"

        # --- 2. Preparação dos Diretórios ---
        diretorio_origem = os.path.dirname(caminho_arquivo)
        novo_diretorio = os.path.join(diretorio_origem, SUBPASTA_DESTINO)

        # Cria a subpasta de destino se ela ainda não existir
        if not os.path.exists(novo_diretorio):
            os.makedirs(novo_diretorio)

        # --- 3. Verificação de Unicidade e Movimentação ---
        
        # Verifica se o arquivo já existe e, se necessário, gera um nome único
        novo_nome_unico = gerar_nome_unico(novo_diretorio, nome_destino)
        novo_caminho = os.path.join(novo_diretorio, novo_nome_unico)

        # A função os.rename() realiza a renomeação e a movimentação (operação atômica)
        try:
            os.rename(caminho_arquivo, novo_caminho)
            print(f"✏️  Arquivo renomeado e movido para: {novo_caminho}")
        except Exception as e:
            # Captura exceções como PermissionError ou FileNotFoundError
            print(f"Erro ao renomear ou mover o arquivo {caminho_arquivo}: {e}")


if __name__ == "__main__":
    # --- Configuração de Execução ---
    
    # ⚠️ ALERTA: Defina o caminho da pasta que será monitorada (Formato Linux/Unix)
    caminho_da_pasta = "/caminho/para/a/pasta" 
    
    # Encerra o script se o caminho não for válido
    if not os.path.exists(caminho_da_pasta):
        print(f"❌ O caminho {caminho_da_pasta} não existe.")
        exit(1)
    
    # Inicialização dos componentes do watchdog
    manipulador_de_eventos = MeuMonitor()
    observador = Observer()
    
    # Agenda o monitoramento. recursive=True monitora subdiretórios também.
    observador.schedule(manipulador_de_eventos, caminho_da_pasta, recursive=True)
    
    # Inicia o observador em uma thread separada para não bloquear o programa principal
    observador.start()
    
    print(f"🚀 Monitorando a pasta '{caminho_da_pasta}'...")
    print("Pressione CTRL+C para parar o monitoramento.")
    
    # Loop principal para manter a thread do observador rodando
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Intercepta o sinal CTRL+C para parar o observador de forma limpa
        observador.stop()
        print("\n⏹️  Monitoramento parado.")
    
    # Garante que a thread do observador finalize antes que o script termine
    observador.join()
