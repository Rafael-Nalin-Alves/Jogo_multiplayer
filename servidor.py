import socket
import threading 
import pickle
import sys
import time

# Classe que armazena os dados de um jogador, como posição, direção e estado de ataque
class JogadorDados:
    def __init__(self, player_id, x, y):
        self.id = player_id  # Identificador único do jogador
        self.x = x  # Posição X inicial
        self.y = y  # Posição Y inicial
        self.direcao = "direita" if player_id == 0 else "esquerda"  # Define direção inicial com base no ID
        self.acao = "idle"  # Estado inicial do jogador (parado)
        self.ataque = {  # Dados relacionados aos ataques
            "ataque1": False,  # Estado do primeiro ataque
            "ataque2": False,  # Estado do segundo ataque
            "velocidade_ataque": 0,  # Velocidade da animação de ataque
            "ataque_x": 0,  # Posição X do ataque
            "ataque_y": 0,  # Posição Y do ataque
            "direcao": "direita" if player_id == 0 else "esquerda"  # Direção do ataque
        }

# Classe principal do servidor do jogo
class ServidorJogo:
    def __init__(self):
        # Inicializa dois jogadores com posições iniciais diferentes
        self.jogadores = [
            JogadorDados(0, 50, 50),  # Jogador 1
            JogadorDados(1, 200, 50)  # Jogador 2
        ]
        # Cria um socket UDP
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Vincula o socket à porta 5555 em todas as interfaces de rede
        self.server.bind(("0.0.0.0", 5555))
        self.encerrar_servidor = False  # Flag para controlar o encerramento do servidor
        self.clientes = {}  # Dicionário para armazenar endereços dos clientes (IP, porta) e seus IDs
        
        # Obtém o endereço IP da máquina para informar ao usuário
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"[SERVIDOR] Aguardando conexões na porta 5555...")
        print(f"[SERVIDOR] Conecte-se usando o IP: {ip_address}")
        print(f"[SERVIDOR] Digite 'quit' a qualquer momento para encerrar o servidor")

    # Método que gerencia a comunicação com os clientes
    def handle_clients(self):
        while not self.encerrar_servidor:
            try:
                # Recebe dados de qualquer cliente (máximo de 2048 bytes)
                data, addr = self.server.recvfrom(2048)
                
                # Verifica se é um novo cliente
                if addr not in self.clientes:
                    if len(self.clientes) < 2:  # Limita a 2 jogadores
                        player_id = len(self.clientes)  # Atribui ID baseado na ordem de conexão
                        self.clientes[addr] = player_id
                        print(f"[JOGADOR {player_id + 1} CONECTADO] {addr}")
                        
                        # Envia dados iniciais ao novo cliente
                        self.server.sendto(pickle.dumps({
                            "player_id": player_id,
                            "player_data": self.jogadores[player_id].__dict__
                        }), addr)
                    continue
                
                # Obtém o ID do jogador associado ao endereço
                player_id = self.clientes[addr]
                
                # Desserializa os dados recebidos do cliente
                data = pickle.loads(data)
                
                # Atualiza os dados do jogador correspondente com os dados recebidos
                for key, value in data.items():
                    setattr(self.jogadores[player_id], key, value)
                
                # Envia os dados do outro jogador para o cliente
                outro_jogador = self.jogadores[1 - player_id].__dict__
                self.server.sendto(pickle.dumps(outro_jogador), addr)

            except Exception as e:
                print(f"Erro: {str(e)}")
                # Remove o cliente em caso de erro (ex.: desconexão)
                if addr in self.clientes:
                    player_id = self.clientes[addr]
                    print(f"[JOGADOR {player_id + 1} DESCONECTOU] - {str(e)}")
                    del self.clientes[addr]

    # Método para monitorar entrada do teclado (comando 'quit')
    def monitorar_teclado(self):
        while not self.encerrar_servidor:
            entrada = input()
            if entrada.strip().lower() == 'quit':
                print("[SERVIDOR] Recebido comando 'quit'. Encerrando servidor...")
                self.encerrar_servidor = True
                break

    # Método principal para iniciar o servidor
    def iniciar(self):
        # Inicia uma thread para monitorar o teclado
        teclado_thread = threading.Thread(target=self.monitorar_teclado)
        teclado_thread.daemon = True  # Thread será encerrada quando o programa terminar
        teclado_thread.start()

        # Inicia uma thread para gerenciar os clientes
        clientes_thread = threading.Thread(target=self.handle_clients)
        clientes_thread.daemon = True
        clientes_thread.start()

        # Loop principal para manter o servidor ativo
        while not self.encerrar_servidor:
            time.sleep(0.1)

        # Fecha o socket do servidor
        self.server.close()
        print("[SERVIDOR] Servidor encerrado com sucesso.")
        sys.exit(0)

# Ponto de entrada do programa
if __name__ == "__main__":
    servidor = ServidorJogo()
    servidor.iniciar()